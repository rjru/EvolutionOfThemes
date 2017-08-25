from ete3 import Tree
from visualization.layout import *
from toolkit.export import *


t = Tree("(((12537577:0.225504,(12537568:0.000207,12537572:0.001745)NoName:0.465109)NoName:0.244957,((21172003:0.19489,(20738864:0.216673,(23034175:0.209226,(20196867:0.154352,20979621:0.411747)NoName:0.156552)NoName:0.040626)NoName:0.044838)NoName:0.056908,(24138928:0.652124,17645804:0.532924)NoName:0.028183)NoName:0.010732)NoName:0.0080395,((20331902:0.691923,(20553586:0.026142,(20156348:0.004258,17822565:0.000463)NoName:0.095187)NoName:0.609364)NoName:0.000403,19740417:0.675576)NoName:0.0080395);", format=1)


rootedTree = EteTreeToBinaryTree(t)
radialLayout(rootedTree)
jsonTree = treeToJson(rootedTree)

print(jsonTree)

