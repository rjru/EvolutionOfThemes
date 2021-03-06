
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

def getTopDistribution(distribution, threshold):
    topDitribution = {}

    if distribution is not None:
        for i in range(0, len(distribution)):
            if distribution[i] > threshold:
                topDitribution[str(i)] = distribution[i]
          #dict(zip([str(i) for i in range(0, len(tree.getDistributionTheme()))], tree.getDistributionTheme()))
    else:
        topDitribution = ""

    return topDitribution

# to format json
def nodesToJsonPubmed(tree, nodes, metaTheme, venue_to_color):

    constOf = 1500  # constante para multiplicar las distancias porque son muy pequeñas
    if tree != None:
        nodesToJsonPubmed(tree.getLeftChild(), nodes, metaTheme, venue_to_color)
        nodesToJsonPubmed(tree.getRightChild(), nodes, metaTheme, venue_to_color)
        #print(tree.getRootVal())
        # 'Yes' if fruit == 'Apple' else 'No'
        distributionTheme = None if tree.getRootVal()[0] == "i" else metaTheme["distributionThemes"][metaTheme["nameThemes"].index(tree.getRootVal())]
        topicsSumary = None if tree.getRootVal()[0] == "i" else metaTheme["topicsSumary"][metaTheme["nameThemes"].index(tree.getRootVal())]

        #print(tree.getX()[0], "; ", tree.getX()[1])
        nodes.append({"data": {"id": tree.getRootVal(),
                               "label": tree.getRootVal() if tree.getRootVal()[0] != 'i' else '',
                               "topDistribution": getTopDistribution(distributionTheme, 0.001),  # getTopDistribution(tree, umbral)
                               "param_1": topicsSumary[1] if topicsSumary else "",
                               "yearTheme": round(topicsSumary[2], 2) if topicsSumary else "",
                               "param_3": topicsSumary[3] if topicsSumary else "",
                               "topWords": dict((y, x) for x, y in topicsSumary[5]) if topicsSumary else "",
                               "topVenue": dict((y, x) for x, y in topicsSumary[6]) if topicsSumary else "",
                               "class": "grey" if tree.getRootVal()[0] == "i" else venue_to_color[topicsSumary[6][0][1]]  # "GreenYellow" #
                               },
                      "position": {"x": constOf * tree.getX()[0], "y": constOf * tree.getX()[1]}
                      }) #json.loads(json.dumps(tree.getExtraInformation()["year"]))
    return nodes

def edgesToJson(tree, edges):
    #if tree != None:
    cons = 1
    if tree.getLeftChild() != None:
        edges.append({"data": {"id": "edge"+str(len(edges)),
                               "source": tree.getLeftChild().getParent().getRootVal(),
                               "target": tree.getLeftChild().getRootVal(),
                               "length": cons*tree.getLeftChild().getweightAristToParentVal()}})
        edgesToJson(tree.getLeftChild(), edges)
    if tree.getRightChild() != None:
        edges.append({"data": {"id": "edge"+str(len(edges)),
                               "source": tree.getRightChild().getParent().getRootVal(),
                               "target": tree.getRightChild().getRootVal(),
                               "length": cons*tree.getRightChild().getweightAristToParentVal()
                               }})
        edgesToJson(tree.getRightChild(), edges)
    return edges

def treeToJsonPubmed(rootedTree, metaDoc, metaTheme, venue_to_color, allJsonDocThemeTop):
    #print('nodes json')
    nodes = []
    nodesJs = nodesToJsonPubmed(rootedTree, nodes, metaTheme, venue_to_color)
    edges = []
    edgesJs = edgesToJson(rootedTree, edges)

#    metaDoc = {"pubmed": pubmed, "pmidToId": pmidToId,
              # "idToPmid": idToPmid, "distributionDoc": docsDescript
              # }

    for idDoc in metaDoc["pubmed"].docs:
        metaDoc["pubmed"].docs[idDoc].pop("abstract")  # remove abstract of document because it is overload json file
        metaDoc["pubmed"].docs[idDoc].pop("filePath")  # remove abstract of document because it is overload json file

        metaDoc["pubmed"].docs[idDoc]["title"] = metaDoc["pubmed"].docs[idDoc]["title"].replace("\"", " ").replace("'", " ")

        if "citLst" in metaDoc["pubmed"].docs[idDoc]:
            metaDoc["pubmed"].docs[idDoc].pop("citLst")

    #cont = 0
    #long = len(metaDoc["pubmed"].docs)
    #for idDoc in metaDoc["pubmed"].docs:
    #    metaDoc["pubmed"].docs[str(idDoc)] = metaDoc["pubmed"].docs.pop(idDoc)
    #    cont = cont + 1

    metaDocDic = {str(key): metaDoc["pubmed"].docs[key] for key in metaDoc["pubmed"].docs}
    idToPmidDict = {str(key): metaDoc["idToPmid"][key] for key in metaDoc["idToPmid"]}
    idDocOrdened = {str(key): metaDoc["idDocOrdened"][key] for key in metaDoc["idDocOrdened"]}

    jsonTree = {"nodes": nodesJs, "edges": edgesJs, "metaDoc": metaDocDic, "idToPmid": idToPmidDict, "idDocOrdened": idDocOrdened, "docDates": metaDoc["datesDoc"], "njInNode": allJsonDocThemeTop}

    return str(jsonTree).replace("'", '"')

#    metaDoc = {"pubmed": pubmed, "pmidToId": pmidToId,
#               "idToPmid": idToPmid, "distributionDoc": docsDescript, "idDocOrdened": idDocOrdened, "datesDoc": datesDoc
#               }

# to format json by document
def nodesToJsonPubmedDoc(tree, nodes, metaDoc, venue_to_color):
    constOf = 1500  # constante para multiplicar las distancias porque son muy pequeñas
    if tree != None:
        nodesToJsonPubmedDoc(tree.getLeftChild(), nodes, metaDoc, venue_to_color)
        nodesToJsonPubmedDoc(tree.getRightChild(), nodes, metaDoc, venue_to_color)
        #print(tree.getRootVal())
        # 'Yes' if fruit == 'Apple' else 'No'
        # arreglar el .index para documentos
        #distributionDoc = None if tree.getRootVal()[0] == "i" else metaDoc["distributionDoc"][metaDoc["nameThemes"].index(tree.getRootVal())]
        #topicsSumary = None if tree.getRootVal()[0] == "i" else metaDoc["topicsSumary"][metaDoc["nameThemes"].index(tree.getRootVal())]
        #print(tree.getX()[0], "; ", tree.getX()[1])
        nodes.append({"data": {"id": tree.getRootVal(),
                               "label": tree.getRootVal() if tree.getRootVal()[0] != 'i' else '',
                               #"topDistribution": getTopDistribution(distributionTheme, 0.001),  # getTopDistribution(tree, umbral)
                               "class": "grey" if tree.getRootVal()[0] == "i" else venue_to_color[metaDoc["pubmed"].docs[int(tree.getRootVal())]["venue"]]
                               #"class": "grey" if tree.getRootVal()[0] == "i" else venue_to_color[topicsSumary[6][0][1]]
                               },
                      "position": {"x": constOf * tree.getX()[0], "y": constOf * tree.getX()[1]}
                      }) #json.loads(json.dumps(tree.getExtraInformation()["year"]))
    return nodes

def edgesToJsonDoc(tree, edges):
    #if tree != None:
    cons = 1
    if tree.getLeftChild() != None:
        edges.append({"data": {"id": "edge"+str(len(edges)),
                               "source": tree.getLeftChild().getParent().getRootVal(),
                               "target": tree.getLeftChild().getRootVal(),
                               "length": cons*tree.getLeftChild().getweightAristToParentVal()}})
        edgesToJson(tree.getLeftChild(), edges)
    if tree.getRightChild() != None:
        edges.append({"data": {"id": "edge"+str(len(edges)),
                               "source": tree.getRightChild().getParent().getRootVal(),
                               "target": tree.getRightChild().getRootVal(),
                               "length": cons*tree.getRightChild().getweightAristToParentVal()
                               }})
        edgesToJson(tree.getRightChild(), edges)
    return edges

def treeToJsonPubmedDoc(rootedTree, metaDoc, metaTheme, venue_to_color):
    #print('nodes json')
    nodes = []
    nodesJs = nodesToJsonPubmedDoc(rootedTree, nodes, metaDoc, venue_to_color)
    edges = []
    edgesJs = edgesToJsonDoc(rootedTree, edges)

    jsonTree = {"nodes": nodesJs, "edges": edgesJs}
    #return str(jsonTree).replace("'", '"')
    return jsonTree

# time series
def nodesToJsonTimeSeries(tree, nodes, vectorTS, label_group, scalaColor):

    constOf = 10  # constante para multiplicar las distancias porque son muy pequeñas
    if tree != None:
        nodesToJsonTimeSeries(tree.getLeftChild(), nodes, vectorTS, label_group, scalaColor)
        nodesToJsonTimeSeries(tree.getRightChild(), nodes, vectorTS, label_group, scalaColor)

        nodes.append({"data": {"id": tree.getRootVal(),
                               "label": tree.getRootVal() if tree.getRootVal()[0] != 'i' else '',
                                "vectorTS": "" if tree.getRootVal()[0] == "i" else dict(zip([str(i) for i in range(0, len(vectorTS[int(tree.getRootVal())]))], vectorTS[int(tree.getRootVal())])),
                               "class": "grey" if tree.getRootVal()[0] == "i" else "rgb"+str(scalaColor[int(label_group[int(tree.getRootVal())])-1])
                               },
                      "position": {"x": constOf * tree.getX()[0], "y": constOf * tree.getX()[1]}
                      }) #json.loads(json.dumps(tree.getExtraInformation()["year"]))
    return nodes

def treeToJsonTimeSeries(rootedTree, vectorTS, label_group, scalaColor):
    nodes = []
    nodesJs = nodesToJsonTimeSeries(rootedTree, nodes, vectorTS, label_group, scalaColor)
    edges = []
    edgesJs = edgesToJson(rootedTree, edges)

    jsonTree = {"nodes": nodesJs, "edges": edgesJs}

    return str(jsonTree).replace("'", '"')