import csv
from clustering_process.clustering import *
from clustering_process.distances import *
from time_series.dimensional_reduction import *
import numpy as np
from sklearn import preprocessing

carpet_dataset = "C:/Users/rbrto-pc/Documents/DATASETS_TIMESERIES/UCR_TS_Archive_2015/"

#source_data_test = "synthetic_control/synthetic_control_TEST"
#source_data_train = "synthetic_control/synthetic_control_TRAIN"

dataset_name = "FacesUCR"
number_class = 14
source_data_test = dataset_name+"/"+dataset_name+"_TEST"
source_data_train = dataset_name+"/"+dataset_name+"_TRAIN"

#Plane, coffee, DiatomSizeReduction, FacesUCR, ItalyPowerDemand, Symbols, Meat

data_test = csv.reader(open(carpet_dataset+source_data_test), delimiter=',')
data_train = csv.reader(open(carpet_dataset+source_data_train), delimiter=',')

label_group = []
ts_dataset = []


def standardize(dataset):
    data = dataset.T
    data_norm = preprocessing.scale(data)
    dataset = data_norm.T
    return dataset

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
# fin de normalización no esta hecho por files o columnas, esta hecho la matriz como conjunto

#name_ts_reduction = ["dct", "dwt", "svd", "cp", "paa", "autoenoders"]
name_ts_reduction = ["none"]
for nametec in name_ts_reduction:
    ts_dataset_reduce = dimensional_reduction(ts_dataset, nametec, 50)
    # normalizamos
    dis_matrix = getMatrixDist(ts_dataset_reduce, DTWDistance)  # DTWDistance dist_euclidean
    t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])

    rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
    radialLayout(rootedTree)

    scalaColor = scale_colors(number_class)
    #print(scalaColor)
    jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset_vis, label_group, scalaColor)
    jsonfile = open(dataset_name+"_"+nametec+"__"+"DTW_train.json", 'w')
    # print(jsonTree)
    jsonfile.write(jsonTree)

'''
# sin reduccion de dimensionalidad
dis_matrix = getMatrixDist(ts_dataset_norm, DTWDistance)
t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])

rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
radialLayout(rootedTree)

scalaColor = scale_colors(6)
#print(scalaColor)
jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset_vis, label_group, scalaColor)
jsonfile = open("C:/Users/rbrto-pc/Google Drive/citation_lda/src/cytoscape/main_visual/data/syntetic_control_300.json", 'w')
# print(jsonTree)
jsonfile.write(jsonTree)
'''