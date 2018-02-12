import csv
from clustering_process.clustering import *
from clustering_process.distances import *
from time_series.dimensional_reduction import *
import numpy as np
from sklearn import preprocessing
import timeit
from fastdtw import fastdtw

def standardize(dataset):
    data = dataset.T
    data_norm = preprocessing.scale(data)
    dataset = data_norm.T
    return dataset

carpet_dataset = "C:/Users/rbrto-pc/Documents/DATASETS_TIMESERIES/UCR_TS_Archive_2015/"
carpet_result = "C:/Users/rbrto-pc/Google Drive/citation_lda/src/cytoscape/main_visual/data/"

dataset_name = "eeg_sleep"
#source_data_test = dataset_name+"/"+dataset_name+"_TEST"
#source_data_train = dataset_name+"/"+dataset_name+"_TRAIN"
source_data_train = dataset_name+"/"+dataset_name+"_TRAIN"

num_dim = 60
num_dim = 6
#Plane, coffee, DiatomSizeReduction, FacesUCR, ItalyPowerDemand, Symbols, Meat

#data_test = csv.reader(open(carpet_dataset+source_data_test), delimiter=',')
data_train = csv.reader(open(carpet_dataset+source_data_train), delimiter=',')

label_group = []
ts_dataset = []

#for row in data_test:
#    label_group.append(row[0])
#    ts_dataset.append([float(i) for i in row[1:]])

for row in data_train:
    label_group.append(row[0])
    ts_dataset.append([float(i) for i in row[1:]])

ts_dataset_norm = standardize(np.array(ts_dataset))

ts_dataset_vis = np.array(ts_dataset)
xmax, xmin = ts_dataset_vis.max(), ts_dataset_vis.min()
ts_dataset_vis = (ts_dataset_vis - xmin)/(xmax - xmin)

print("distance matrix calculation")
dis_matrix = getMatrixDist(ts_dataset_vis, fastdtw)  # DTWDistance dist_euclidean
a = numpy.asarray(dis_matrix)
numpy.savetxt("dis_matrix_time_series_eeg.csv", a, delimiter=",")
print('ACABO CALCULO DE MATRIZ DE DISTANCIA')
t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])
rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
radialLayout(rootedTree)

scalaColor = scale_colors(6)
# print(scalaColor)
jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset_vis, label_group, scalaColor)
jsonfile = open("../clustering_process/result/eeg_sleep.json", 'w')
# print(jsonTree)
jsonfile.write(jsonTree)