# Usando toda la serie temporal
#import sys


#from keras.layers import Input, Dense
#from keras.models import Model
import numpy as np
import pandas as pd
#from sklearn.metrics import mean_squared_error
#import functionsAE

from random import randint

import random

#from sklearn.preprocessing import MinMaxScaler
from scipy.fftpack import dct, idct

from sklearn import preprocessing

class DCT:
	def __init__(self):
		self.dataset = []
		#self.encoding_dim = 10
		self.id = [] 

		self.activations =[] 

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
		i = self.dataset.shape[0]-1
		while (i>=0):
			j = randint(0, i)

			temp = list(self.dataset[i])
			self.dataset[i] = list(self.dataset[j])
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
		data_norm = preprocessing.scale(data)
		self.dataset = data_norm.T

	def execute_dct(self,dim):
		#print self.dataset.shape
		#print 'self.dataset[0] = ', self.dataset[0]

		self.activations = dct(self.dataset, norm='ortho')[:,0:dim]
		#print self.activations.shape

		#self.activations = self.encoder.predict(self.dataset)

	def sort_coefficients(self):
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

	def save_activations(self, filename):
		f = open(filename,'w')
		# f.write(filename)
		# f.write(', ')
		np.savetxt(f, self.activations, delimiter=",")
		f.close()
		#print 'Saved!'
	
	def get_coefficients(self):
		return self.activations

''' total = len(sys.argv)
cmdargs = (sys.argv)

if total>1:
	filename = 'caract_'+str(cmdargs[1])
else:
	filename = 'caract_dct'

for i in range(60):
	dcost = DCT()
	dcost.load_data('dataset.csv')
	#dcost.load_data('dataset.csv')
	dcost.shuffle_data()
	#dcost.normalize() 
	dcost.standardize()
	dcost.execute_dct(i+1)
	dcost.sort_coefficients()
	dcost.save_activations(filename+'_'+str(i+1)+'.csv')
	#dcost.save_activations('caract_dct.csv')

print filename+' [ok]'
'''
