# Usando toda la serie temporal
import sys

#from keras.layers import Input, Dense
#from keras.models import Model
import numpy as np
import pandas as pd
#from sklearn.metrics import mean_squared_error
#import functionsAE

from random import randint

import random

#from sklearn.preprocessing import MinMaxScaler

from sklearn import preprocessing

class CP:
	def __init__(self):
		self.dataset = []
		#self.encoding_dim = 10
		self.id = [] 

		self.activations =[]

		self.I = []


	def load_data(self, data):
		#self.dataset = pd.read_csv(filename, delim_whitespace=True, header=None)
		#self.dataset = pd.read_csv(filename, header=None) # 600 x 60
		self.dataset = data
		self.dataset = np.array(self.dataset)
		for i in range(self.dataset.shape[0]):
			self.id.append(i)

		# self.I = np.zeros(self.dataset.shape[1])
		N=self.dataset.shape[1]
		self.I = np.zeros(N+1)
		self.I[0] = -1.0
		for i in range(1,N):
			self.I[i] = (2.0*i-1.0)/(N-1.0)-1.0
		self.I[N]=1.0
		#print 'I = ', self.I
		#self.I = np.linspace(-1,1,self.dataset.shape[1]+1)

	def set_data(self, data):
		self.dataset = data
		for i in range(self.dataset.shape[0]):
			self.id.append(i)

		N=self.dataset.shape[1]
		self.I = np.zeros(N+1)
		self.I[0] = -1.0
		for i in range(1,N):
			self.I[i] = (2.0*i-1.0)/(N-1.0)-1.0
		self.I[N]=1.0

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

	def w(self, t):
		return 1/np.sqrt(1-t*t)

	def f(self, t):
		i=1
		while i<=self.dataset.shape[1] and t>=self.I[i]:
			i = i + 1
		length = self.I[i]-self.I[i-1]
		return self.dataset[:,i-1]/np.sqrt(self.w(t)*length)

	def P(self, i, t):
		return np.cos(i*np.arccos(t))

	def cp(self, data, dim):		
		x = data
		N = data.shape[1]

		t = np.zeros(N)
		for j in range(N):
			t[j]=np.cos(((j+1)-0.5)*np.pi/N)
		
		c = np.zeros((data.shape[0],dim))
		for i in range(dim):
			for j in range(N):
				c[:,i] = c[:,i] + self.f(t[j])*self.P(i,t[j])
			if i==0:
				c[:,i] = c[:,i]/N
			else:
			 	c[:,i] = 2.0*c[:,i]/N
			#r[:,i] = x[:,(L*i):(L*(i+1))].sum(axis=1)/L
		return c

	def execute_cp(self, dim):
		#print self.dataset.shape
		#print 'self.dataset[0] = ', self.dataset[0]

		self.activations = self.cp(self.dataset, dim)
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

'''
total = len(sys.argv)
cmdargs = (sys.argv)

if total>1:
	filename = 'caract_'+str(cmdargs[1])
else:
	filename = 'caract_cp'

for i in range(60):
	cp = CP()
	cp.load_data('dataset.csv')
	#cp.load_data('dataset.csv')
	cp.shuffle_data()
	#cp.normalize(-1.0, 1.0)
	cp.standardize()
	cp.execute_cp(i+1)
	cp.sort_coefficients()
	cp.save_activations(filename+'_'+str(i+1)+'.csv')
	#cp.save_activations('caract_cp.csv')

'''