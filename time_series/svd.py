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

from sklearn.preprocessing import MinMaxScaler
from scipy.fftpack import dct, idct
#import pywt

from sklearn import preprocessing


class SVD:
	def __init__(self):
		self.dataset = []
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

	def paa(self, data):		
		x = data
		N = data.shape[1]
		M = 10
		L = int(N/M)
		r = np.zeros((data.shape[0],M))
		for i in range(M):
			r[:,i] = x[:,(L*i):(L*(i+1))].sum(axis=1)/L
		return r

	def get_symbol(self, x, alphabet_size):
		i = 0
		while i<(alphabet_size-1):
			if x<(self.lookuptable[i, alphabet_size-3]):
				return i
			i = i +1
		return i

	def run_svd(self, dim):
		x=self.dataset.T		
		U,s,V = np.linalg.svd(x,full_matrices=True)
		S=np.zeros(x.shape)
		S[:s.shape[0],:s.shape[0]] = np.diag(s)
		self.activations = np.dot(S[:dim,:],V).T

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
	filename = 'caract_svd'

for i in range(60):
	svd = SVD()
	svd.load_data('dataset.csv')
	#svd.load_data('dataset.csv')
	svd.shuffle_data()
	#svd.normalize()
	svd.standardize()
	#svd.s1()
	svd.run_svd(i+1)
	svd.sort_coefficients()
	#svd.save_activations('caract_'+svd.__class__.__name__.lower()+'60.csv')
	svd.save_activations(filename+'_'+str(i+1)+'.csv')
	#svd.save_activations('caract_svd.csv')
print filename+' [ok]'
'''