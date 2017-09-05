import csv
from clustering_process.clustering import *
from clustering_process.distances import *
import numpy as np

carpet_dataset = "C:/Users/rbrto-pc/Documents/DATASETS_TIMESERIES/UCR_TS_Archive_2015/"
source_data_test = "synthetic_control/synthetic_control_TEST"
source_data_train = "synthetic_control/synthetic_control_TRAIN"

data_test = csv.reader(open(carpet_dataset+source_data_test), delimiter=',')
data_train = csv.reader(open(carpet_dataset+source_data_train), delimiter=',')

label_group = []
ts_dataset = []

#for row in data_test:
#    label_group.append(row[0])
#    ts_dataset.append([float(i) for i in row[1:]])

for row in data_train:
    label_group.append(row[0])
    ts_dataset.append([float(i) for i in row[1:]])

#label_group = label_group[0:50]
#ts_dataset = ts_dataset[0:50]

# normalizamos
ts_dataset = np.array(ts_dataset)
xmax, xmin = ts_dataset.max(), ts_dataset.min()
ts_dataset = (ts_dataset - xmin)/(xmax - xmin)
# fin de normalización no esta hecho por files o columnas, esta hecho la matriz como conjunto

dis_matrix = getMatrixDist(ts_dataset, DTWDistance)
t = njWithRoot(dis_matrix, [i for i in range(0, len(ts_dataset))])

rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
radialLayout(rootedTree)

scalaColor = scale_colors(6)
print(scalaColor)
jsonTree = treeToJsonTimeSeries(rootedTree, ts_dataset, label_group, scalaColor)
jsonfile = open("res.json", 'w')
# print(jsonTree)
jsonfile.write(jsonTree)