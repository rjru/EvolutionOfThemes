
from corpus.pubmed import *
import topic_modeling.lda
import numpy
from toolkit.export import matrix_to_pex
from theme_discovery.citation_based_method import readTopicSummary
from toolkit.vis_vector import *
from skbio import DistanceMatrix
from skbio.tree import nj
from toolkit.utility import *
from visualization.layout import *
from toolkit.export import *

from clustering_process.distances import *

# each document has a set of themes buy they are in disorden. This method sorted themes by date
def getThemesOrdened(topicsSumary):
    datesThemes = []
    idThemeOrdened = []
    for k in sorted(topicsSumary, key=lambda k: topicsSumary[k][2]):
        idThemeOrdened.append(k)  # for example idThemeOrdened[0] = 13 and with the same id 0 in datesTheme[0] = 1990.18 it is the minimum value
        datesThemes.append(topicsSumary[k][2])
    return (idThemeOrdened, datesThemes)
# this method ordened each descriptor of themes of each document by date
def getThemesOfDocsOrdered(listIdPmid, idThemeOrdened):
    docsThemesOrdened = []
    for doc in listIdPmid:
        docOrd = []
        for idOrd in idThemeOrdened:
            docOrd.append(doc[idOrd])
        docsThemesOrdened.append(docOrd)
    return docsThemesOrdened

def getMatrixDist(docsThemesOrdened, distance_method):
    lenMuesta = len(docsThemesOrdened)
    dis_matrix = numpy.zeros((lenMuesta, lenMuesta))

    for v1 in range(0, lenMuesta):
        for v2 in range(0, lenMuesta):
            dis_matrix[v1][v2] = distance_method(docsThemesOrdened[v1], docsThemesOrdened[v2])

    return dis_matrix

def njWithRoot(dis_matrix, muestraPmid):
    # no culcula la distancia, solo le da un formato mas adecuado a las distancias con los ids
    muestraPmidStr = [str(i) for i in muestraPmid]
    dm = DistanceMatrix(dis_matrix.tolist(), muestraPmidStr)
    treeOrig = nj(dm, result_constructor=str)
    # ponerle raiz
    t = Tree(treeOrig)
    R = t.get_midpoint_outgroup()
    t.set_outgroup(R)
    # imprime el arbol
    #print(t)
    # imprime el newick
    tree = t.write(format=3)
    tree = Tree(tree, format=1)
    #print(tree)
    #a = newick_to_pairwise_nodes(tree)
    #print(a)
    return tree

if __name__ == '__main__':
    pubmed = getPubMedCorpus()  # load raw data
    #print(pubmed.docs[21172003])
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pubmed)
    ldaFilePath = os.path.join(variables.TEST_RESULT, 'pubmed_citation_lda_40_5001_5001_0.001_0.001_timeCtrl_3_4.5.lda')
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath)  # load lda result
    ldaTopicSumaryFilePath = os.path.join(variables.TEST_RESULT, 'pubmed_citation_lda_40_5001_5001_0.001_0.001_timeCtrl_3_4.5.lda_summary')
    topicsSumary = readTopicSummary(ldaTopicSumaryFilePath)  # load lda sumary for order descriptor by time

    # we get characteristic description of each document, this was calculated by lda before
    # the detail is that descriptor is in disorder
    docsDescript = ldaInstance.thetaEstimate  # the descriptor of each document is conformed by a set of themes
    themesDescript = ldaInstance.phiEstimate  # the descriptor of each themes is conformed by a set of citation
    (idThemeOrdened, datesThemes) = getThemesOrdened(topicsSumary)  # idThemeOrdened are ids that are ordened by time and dataThemes are dates ordened by time

    # these are data examples, in another words these are a little data for make test
    muestraPmid = [21172003, 17822565, 20553586, 20156348, 20331902, 19740417, 20979621, 20738864, 20196867, 12537577,
                   17645804, 12537572, 12537568, 24138928, 23034175]

    muestraIdPmid = []
    for Mpmid in muestraPmid:
        distribution = ldaInstance.thetaEstimate[pmidToId[Mpmid]]
        muestraIdPmid.append(distribution)
    # these are data example

    print('ordened vector')
    docsThemesOrdened = getThemesOfDocsOrdered(muestraIdPmid, idThemeOrdened)  # docsDescript  muestraIdPmid
    print('calculate matrix distance')
    #dis_matrix = getMatrixDist(docsThemesOrdened, dist_euclidean) # for document
    dis_matrix = getMatrixDist(themesDescript, dist_euclidean)  # for themes
    #print('generate image of document')
    #generateImageDistribution(docsThemesOrdened, datesThemes, list(idToPmid.values()))  # muestraPmid generate image about themes' distribution of each document

    #print('generate image of themes')
    # None pues en el caso de los temas solo es necesario las coordenadas del eje y
    #generateImageDistribution(themesDescript, None, [i for i in range(0, len(themesDescript))])  # muestraPmid generate image about themes' distribution of each document

    #print('save result pex format')
    #res = matrix_to_pex('matrix_of_docs', dis_matrix, muestraPmid)

    # método para aplicar nj y ademas calcula la raiz, mejor dicho lo convierte en un árbol con raiz
    #t = njWithRoot(dis_matrix, muestraPmid) # for document

    nameThemes = []
    for theme in range(0, len(themesDescript)):
        nameThemes.append("theme_"+str(theme))

    t = njWithRoot(dis_matrix, nameThemes) # for themes
    #print(t)
    # EteTreeToBinaryTree([t:resultado del NJ], [pubmed:citMetaGraph,docs], [nombres de elementos],
    metaDoc = {"pubmed": pubmed, "pmidToId": pmidToId,
               "idToPmid": idToPmid, "distributionDoc": docsDescript,
               "muestraPmid": muestraPmid
               }
    metaTheme = {"topicsSumary": topicsSumary, "distributionThemes": themesDescript,
                 "idThemeOrdened": idThemeOrdened, "datesThemes": datesThemes, "nameThemes": nameThemes
                 }


    rootedTree = EteTreeToBinaryTree(t, metaDoc, metaTheme) # since now, we use only themes
    radialLayout(rootedTree)
    jsonTree = treeToJson(rootedTree)
    jsonfile = open("res.json", 'w')
    #print(jsonTree)
    jsonfile.write(jsonTree)