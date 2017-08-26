
import os
from toolkit import variables
import json
def matrix_to_pex(name, matrix_dist, list_namefiles):
    pwd = os.path.join(variables.TEST_RESOURCE, 'exportToPex/')
    f = open(pwd+name+'.dmat', 'w')
    f.write(str(len(matrix_dist)))
    f.write("\n")

    # write the names
    for i in range(0, len(list_namefiles)):
        if i == len(list_namefiles) - 1:
            f.write(str(list_namefiles[i]))
        else:
            f.write(str(list_namefiles[i]) + "; ")
    f.write("\n")

    # here write the class of each document but in pubmed database haven't classes then only write 0.0
    for i in range(0, len(list_namefiles)):
        # esta forma es comprando la primera letra del nombre para ver a cual clase pertenece no es la mejor forma pero es rapida
        if i == len(list_namefiles) - 1:
            f.write("0.0")
        else:
            f.write("0.0; ")

    # here write the matrix dist
    count = 0
    for i in range(0, len(matrix_dist)):
        for j in range(0, len(matrix_dist)):
            if i > j:
                count = count + 1
                if j == i - 1:
                    f.write(str(matrix_dist[i][j]))
                else:
                    f.write(str(matrix_dist[i][j]) + "; ")  # python will convert \n to os.linesep
        f.write("\n")
    f.close()  # you can omit in most cases as the destructor will call it

# to format json
def nodesToJson(tree, nodes):
    constOf = 10 # constante para multiplicar las distancias porque son muy pequeñas
    if tree != None:
        nodesToJson(tree.getLeftChild(), nodes)
        nodesToJson(tree.getRightChild(), nodes)
        #print(tree.getRootVal())
        # 'Yes' if fruit == 'Apple' else 'No'
        nodes.append({"data": {"id": tree.getRootVal(),
                               "label": tree.getRootVal() if tree.getRootVal()[0] != 'i' else '',
                               "extraInfo": dict(zip([str(i) for i in range(0, len(tree.getDistributionTheme()))], tree.getDistributionTheme())) if tree.getDistributionTheme() != None else ""
                               },
                      "position": {"x": constOf * tree.getX()[0], "y": constOf * tree.getX()[1]}
                      }) #json.loads(json.dumps(tree.getExtraInformation()["year"]))
    return nodes

def edgesToJson(tree, edges):
    #if tree != None:
    if tree.getLeftChild() != None:
        edges.append({"data": {"id": len(edges), "source": tree.getLeftChild().getParent().getRootVal(), "target": tree.getLeftChild().getRootVal(), "length": 10*tree.getLeftChild().getweightAristToParentVal()}})
        edgesToJson(tree.getLeftChild(), edges)
    if tree.getRightChild() != None:
        edges.append({"data": {"id": len(edges),
                               "source": tree.getRightChild().getParent().getRootVal(),
                               "target": tree.getRightChild().getRootVal(),
                               "length": 10*tree.getRightChild().getweightAristToParentVal()
                               }})
        edgesToJson(tree.getRightChild(), edges)
    return edges

def treeToJson(rootedTree):
    #print('nodes json')
    nodes = []
    nodesJs = nodesToJson(rootedTree, nodes)
    #print('edges json')
    edges = []
    edgesJs = edgesToJson(rootedTree, edges)

    jsonTree = {"nodes": nodesJs, "edges": edgesJs}
    # print(str(jsonTree).replace("'", '"'))
    return str(jsonTree).replace("'", '"')
