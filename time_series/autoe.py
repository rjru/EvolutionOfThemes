# Usando toda la serie temporal
import sys


from keras.layers import Input, Dense
from keras.models import Model
from keras import optimizers
from keras import initializers

import numpy as np
import pandas as pd
#from sklearn.metrics import mean_squared_error
#import functionsAE

import matplotlib.pyplot as plt

from random import randint

import random

from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing


#np.random.seed(123) 

class AUTOE:
	def __init__(self):
		self.dataset = []
		#self.encoding_dim = 10
		self.id = []
		self.x_train = []
		self.x_test = []
		self.activations =[]
		self.autoencoder = []
		self.encoder = []

	def load_data(self, data):
		#self.dataset = pd.read_csv(filename, delim_whitespace=True, header=None)
		#self.dataset = pd.read_csv(filename, header=None) # 600 x 60
		self.dataset = data
		self.dataset = np.array(self.dataset)
		for i in range(self.dataset.shape[0]):
			self.id.append(i)

	def set_data(self, data):
		self.dataset = data
		for i in range(self.dataset.shape[0]):
			self.id.append(i)

	def shuffle_data(self):
		#self.dataset = np.copy(data)
		i = self.dataset.shape[0]-1
		while (i>=0):
			j = randint(0, i)

			temp = np.copy(self.dataset[i])
			self.dataset[i] = np.copy(self.dataset[j])
			self.dataset[j] = temp

			aux = self.id[i]
			self.id[i] = self.id[j]
			self.id[j] = aux

			i = i - 1

	def normalize(self, mini, maxi):
		data = self.dataset.T
		#print 'data.shape =zzz ', data.shape
		data_norm = (data*1.0-data.min(axis=0))/(data.max(axis=0)-data.min(axis=0))
		#scaler = MinMaxScaler(feature_range=(0, 1))
		#data_norm = scaler.fit_transform(data)
		data_norm = data_norm*(maxi-mini)+mini
		self.dataset = data_norm.T

	def standardize(self):
		data = self.dataset.T 
		y = np.copy(data)
		ynorm = (y*1.0-y.mean(axis=0))/y.std(axis=0)
		data_norm = preprocessing.scale(data)
		print (type(ynorm))
		for i in range(ynorm.shape[0]):
			for j in range(ynorm.shape[1]):
				if ynorm[i, j]!=data_norm[i,j]:
					print ('different',i ,'-',  j)
		self.dataset = data_norm.T

	def divide_data(self, prob):
		row = int(round(prob * self.dataset.shape[0]))
		
		self.x_train = self.dataset[:row, :]
		self.x_test = self.dataset[row:, :] 

	def create_autoencoder(self, encoding_dim):
		secuence_dim = self.dataset.shape[1]

		# this is our input placeholder
		n_input = Input(shape=(secuence_dim,))
		#encoded = Dense(encoding_dim, activation='tanh', weights = [np.zeros([60, encoding_dim]), np.zeros(encoding_dim)])(n_input)
		#decoded = Dense(secuence_dim, activation='tanh', weights = [np.zeros([encoding_dim, 60]), np.zeros(60)])(encoded)
		init_values = initializers.RandomNormal(mean=0.0, stddev=0.05, seed=True)
		#init_values = initializers.RandomUniform(minval=-0.05, maxval=0.05, seed=None)
		encoded = Dense(encoding_dim, activation='linear', kernel_initializer=init_values, bias_initializer=init_values)(n_input)
		decoded = Dense(secuence_dim, activation='linear', kernel_initializer=init_values, bias_initializer=init_values)(encoded)

		#print 'initializer', keras.initializers.Initializer()
		# this model maps an input to its reconstruction
		self.autoencoder = Model(input=n_input, output=decoded)

		# this model maps an input to its encoded representation
		self.encoder = Model(input=n_input, output=encoded)

		#print 'sumary: ', self.autoencoder.summary()

		#autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
		#self.autoencoder.compile(optimizer='adadelta', loss='mse') 
		# adam, rmsprop, adadelta, 
		rmsprop = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
		self.autoencoder.compile(optimizer=rmsprop, loss='mse', metrics=['accuracy'])
		#print '\nBefore training ...'
		#for layer in self.autoencoder.layers:
		#	weights = layer.get_weights()
		#	g=layer.get_config()
		#	if len(weights)>0:
		#		print 'get_config= ', g
		#		print 'weights= ', weights
		#		print 'weights[0].shape = ', weights[0].shape
		#		print 'weights[1].shape = ', weights[1].shape

	def train_autoencoder(self):
		hist = self.autoencoder.fit(self.x_train, self.x_train,
            epochs=100,
            batch_size=20,
            shuffle=False,
            verbose=0,
            validation_data=(self.x_test, self.x_test))
		# plot history
		#loss = hist.history['loss']
		#val_loss = hist.history['val_loss']
		#epochs = np.arange(len(loss))
		#plt.plot(epochs, loss, 'bo', label='Train loss')
		#plt.plot(epochs, val_loss, 'r+', label='Test loss')
		#plt.grid()
		#plt.xlabel('Epochs')
		#plt.ylabel('Loss')
		#plt.legend()
		#plt.show()

		#functionsAE.plot_history(loss, 'varObj')
		# Obtaining activations
		self.activations = self.encoder.predict(self.dataset)

	def test_autoencoder(self):
		#decoded_input = self.autoencoder.predict(self.x_test)
		scores = self.autoencoder.evaluate(self.x_test, self.x_test, verbose=0)
		scores_train = self.autoencoder.evaluate(self.x_train, self.x_train, verbose=0)
		#print 'loss = ', scores*100
		print("\nTrain %s: %.2f%%" % (self.autoencoder.metrics_names[0], scores_train[0]*100))
		print("\nTest %s: %.2f%%" % (self.autoencoder.metrics_names[0], scores[0]*100))
		return scores_train[0], scores[0]

	def plot_reconstruction(self):
		print ('Plotting x_test')
		reconstructed_data = self.autoencoder.predict(self.x_test)
		for j in range(1):
			idx = j
			plt.plot(np.arange(60), self.x_test[idx], 'b-', label='Original')
			plt.plot(np.arange(60), reconstructed_data[idx], 'r--', label = 'Reconstructed')
			#plt.title('Features: '+str(title))
			plt.title('Test Data: '+str(self.id[len(self.x_train)+idx])+'-'+self.type_synthetic_chart(self.id[len(self.x_train)+idx]))
			plt.xlabel('x (Time)')
			plt.show()
		print ('Plotting x_train')
		reconstructed_data = self.autoencoder.predict(self.x_train)
		for j in range(1):
			idx = j
			plt.plot(np.arange(60), self.x_train[idx], 'b-', label='Original')
			plt.plot(np.arange(60), reconstructed_data[idx], 'r--', label='Reconstructed')
			#plt.title('Features: '+str(title))
			plt.title('Train Data: '+str(self.id[idx])+'-'+self.type_synthetic_chart(self.id[idx]))
			plt.xlabel('x (Time)')
			plt.show()

	def sort_activations(self):
		for i in range(1,self.activations.shape[0]):
			v=self.id[i]
			temp=list(self.activations[i])
			j=i-1
			while j >= 0 and self.id[j] > v:
				self.id[j+1] = self.id[j]
				self.activations[j+1] = list(self.activations[j])
				j=j-1
			self.id[j+1]=v
			self.activations[j+1]=temp
		#print 'Sorted!'

	def save_activations(self,filename):
		f = open(filename,'w')
		# f.write(filename)
		# f.write(', ')
		np.savetxt(f, self.activations, delimiter=",")
		f.close()
		#print 'Saved!'

	def get_activations(self):
		return self.activations

	def type_synthetic_chart(self, idx):
		type = ['Normal', 'Cyclic', 'Increasing trend', 
		'Decreasing trend', 'Upward shift', 'Downward shift']
		return type[int(idx/100.0)]

'''
total = len(sys.argv)
cmdargs = (sys.argv)

if total>1:
	filename = 'caract_'+str(cmdargs[1])
else:
	filename = 'caract_autoe'

loss_train = np.zeros(60)
loss_test = np.zeros(60)
for i in range(60):
	autoe = AUTOE()
	autoe.load_data('dataset.csv')
	#autoe.load_data('dataset.csv')
	autoe.shuffle_data()	
	#autoe.normalize(-1,1)
	autoe.standardize()
	autoe.divide_data(0.8)
	autoe.create_autoencoder(i+1)
	#autoe.normalize() # best results of clustering for interval [0, 1]
	#autoe.standardize()
	autoe.train_autoencoder()
	
	loss_train[i], loss_test[i] = autoe.test_autoencoder()
	#autoe.get_activations()	
	
	#autoe.plot_reconstruction()
	autoe.sort_activations()
	#autoe.save_activations('caract_autoe.csv')
	autoe.save_activations(filename+'_'+str(i+1)+'.csv')
	#autoe.save_activations('caract_autoe.csv')
	#print 'activations: ', autoe.get_activations()

plt.plot(np.arange(60), loss_train,'bo', label = 'Train loss')
plt.plot(np.arange(60), loss_test, 'r+', label = 'Test loss')
plt.legend()
plt.grid()
plt.xlabel('Feature lenght')
plt.ylabel('Loss')
plt.show()

print 'loss_train', loss_train[[9,19,29,39,49]]
print 'loss_test', loss_test[[9,19,29,39,49]]
'''
