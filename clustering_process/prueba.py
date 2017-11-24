from dtw import dtw
import numpy as np
from dtw import dtw
from scipy.spatial.distance import euclidean


x = np.array([0.2, 0.6, 0.8, 0.9, 0.2, 0.2, 0.3, 0.7, 0.2, 0.4])
y = np.array([0.2, 0.8, 0.2, 0.7, 0.2])

#y = np.array([0.7, 0.3, 0.2, 0.5, 0.6, 0.9, 0.7, 0.0, 0.3, 0.7]) #  el mas diferente
dist, cost, acc, path = dtw(x, y, dist=euclidean)
print(dist)

# another library
from fastdtw import fastdtw
distance, path = fastdtw(x, y, dist=euclidean)
print(distance)

from clustering_process.distances import *
dis = DTWDistance(x, y)
print(dis)