import csv
from clustering_process.clustering import *
from clustering_process.distances import *
from time_series.dimensional_reduction import *
import numpy as np
from sklearn import preprocessing
import timeit


carpet_dataset = "C:/Users/rbrto-pc/Documents/DATASETS_TIMESERIES/UCR_TS_Archive_2015/"
carpet_result = "C:/Users/rbrto-pc/Google Drive/citation_lda/src/cytoscape/main_visual/data/"

#datasetAtrib = {"DiatomSizeReduction": {"num_class": 4, "dimen": 345},
#                              "Trace": {"num_class": 4, "dimen": 275},
#                              "Plane": {"num_class": 7, "dimen": 144}
#                }

dataset_name = "synthetic_control"
source_data_test = dataset_name+"/"+dataset_name+"_TEST"
source_data_train = dataset_name+"/"+dataset_name+"_TRAIN"
num_dim = 60
#Plane, coffee, DiatomSizeReduction, FacesUCR, ItalyPowerDemand, Symbols, Meat

data_test = csv.reader(open(carpet_dataset+source_data_test), delimiter=',')
data_train = csv.reader(open(carpet_dataset+source_data_train), delimiter=',')

def standardize(dataset):
    data = dataset.T
    data_norm = preprocessing.scale(data)
    dataset = data_norm.T
    return dataset

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
# fin de normalización no esta hecho por files o columnas, esta hecho la matriz como conjunto

#name_ts_reduction = ["dct", "dwt", "svd", "cp", "paa", "autoenoders", "none"]
#name_ts_reduction = ["cp"]
reducts = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
result_time = open("result_time.data", "w")

ts_dataset = ts_dataset[0:499]

for reduct in reducts:
    #*************************** EUclidina***********************************************************
    start = timeit.default_timer()
    ts_dataset_reduce = dimensional_reduction(ts_dataset, "paa", int(reduct*num_dim))
    dis_matrix = getMatrixDist(ts_dataset_reduce, dist_euclidean)  # DTWDistance dist_euclidean
    t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])
    rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
    radialLayout(rootedTree)
    stop = timeit.default_timer()

    result_time.write(dataset_name+", "+str(int(reduct*num_dim))+", "+"eucli, "+"paa"+", "+str(stop-start)+"\n")
    scalaColor = scale_colors(2)
    #print(scalaColor)
    jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset_vis, label_group, scalaColor)
    jsonfile = open(carpet_result+dataset_name+"_"+"paa"+"_"+str(int(reduct*num_dim))+"_eucli_total.json", 'w')
    # print(jsonTree)
    jsonfile.write(jsonTree)
    print("name: ", dataset_name, "Name_Tec: ", "paa", " Euclidean", stop-start)

for reduct in reducts:
    #*************************** DWT***********************************************************
    start = timeit.default_timer()
    ts_dataset_reduce = dimensional_reduction(ts_dataset, "paa", int(reduct * num_dim))
    dis_matrix = getMatrixDist(ts_dataset_reduce, DTWDistance)  # DTWDistance dist_euclidean
    t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])
    rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
    radialLayout(rootedTree)
    stop = timeit.default_timer()

    result_time.write(dataset_name + ", " + str(int(reduct * num_dim)) + ", " + "dtw, " + "paa" + ", " + str(stop - start)+"\n")
    scalaColor = scale_colors(2)
    #print(scalaColor)
    jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset_vis, label_group, scalaColor)
    jsonfile = open(carpet_result+dataset_name+"_"+"paa"+"_"+str(int(reduct*num_dim))+"_DTW_total.json", 'w')
    # print(jsonTree)
    jsonfile.write(jsonTree)
    print("name: ", dataset_name, "Name_Tec: ", "paa", " DTW", stop-start)
