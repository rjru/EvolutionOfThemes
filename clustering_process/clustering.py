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
from dtw import dtw
from scipy.spatial.distance import euclidean
from clustering_process.distances import *
from fastdtw import fastdtw
from clustering_process.nj_and_doc2 import *
from ete3 import Tree as TreeEte
# each document has a set of themes buy they are in disorder. This method sorted themes by date
def getIdAndDatesOfThemesOrdered(topicsSumary):
    datesThemes = []
    idThemeOrdened = []
    for k in sorted(topicsSumary, key=lambda k: topicsSumary[k][2]):
        idThemeOrdened.append(k)  # for example idThemeOrdened[0] = 13 and with the same id 0 in datesTheme[0] = 1990.18 it is the minimum value
        datesThemes.append(topicsSumary[k][2])
    return (idThemeOrdened, datesThemes)

def getIdAndDatesOfDocOrdered(ldaInstance, pubmed, idToPmid):
    docAndDate = {}
    for d in range(ldaInstance.D):
        aux = {}
        pmid = idToPmid[d]
        year = pubmed.docs[pmid]['year']
        aux[0] = d
        aux[1] = pmid
        aux[2] = year
        docAndDate[d] = aux

    idDocOrdened = []
    datesDoc = []
    for k in sorted(docAndDate, key=lambda k: docAndDate[k][2]):
        idDocOrdened.append(k)  # for example idThemeOrdened[0] = 13 and with the same id 0 in datesTheme[0] = 1990.18 it is the minimum value
        datesDoc.append(docAndDate[k][2])
    return (idDocOrdened, datesDoc)

# this method ordened each descriptor of themes of each document by date
def getThemesOfDocsOrdered(listIdPmid, idThemeOrdened):
    docsThemesOrdened = []
    for doc in listIdPmid:
        docOrd = []
        for idOrd in idThemeOrdened:
            docOrd.append(doc[idOrd])
        docsThemesOrdened.append(docOrd)
    return docsThemesOrdened

def getDocOfThemesOrdered(idDocOrdened, themesDescript):
    DocOfThemesOrdered = []
    for theme in themesDescript:
        aux = []
        for i in range(0, len(theme)):
            aux.append(theme[idDocOrdened[i]])
        DocOfThemesOrdered.append(aux)
    return DocOfThemesOrdered

def getMatrixDist(docsThemesOrdened, distance_method):
    lenMuesta = len(docsThemesOrdened)
    dis_matrix = numpy.zeros((lenMuesta, lenMuesta))

    for v1 in range(0, lenMuesta):
        for v2 in range(0, lenMuesta):
            print("\r In {} Loading... {}".format(v1, v2), end="")
            if v1 == v2:
                dis_matrix[v1][v2] = 0
            if v1 < v2:
                dist_temp, path = distance_method(docsThemesOrdened[v1], docsThemesOrdened[v2], dist=euclidean)
                #dist_temp, var = distance_method(docsThemesOrdened[v1], docsThemesOrdened[v2])
                dis_matrix[v1][v2] = dist_temp
                dis_matrix[v2][v1] = dist_temp

    return dis_matrix

# raise DistanceMatrixError("Data must be hollow (i.e., the diagonal" skbio.stats.distance._base.DistanceMatrixError: Data must be hollow (i.e., the diagonal can only contain zeros).

def njWithRoot(dis_matrix, muestraPmid):
    # no culcula la distancia, solo le da un formato mas adecuado a las distancias con los ids
    muestraPmidStr = [str(i) for i in muestraPmid]
    ver = dis_matrix.tolist()
    dm = DistanceMatrix(ver, muestraPmidStr)
    treeOrig = nj(dm, result_constructor=str)
    # ponerle raiz
    t = TreeEte(treeOrig)
    R = t.get_midpoint_outgroup()
    t.set_outgroup(R)
    # imprime el arbol
    #print(t)
    # imprime el newick
    tree = t.write(format=3)
    tree = TreeEte(tree, format=1)
    #print(tree)
    #a = newick_to_pairwise_nodes(tree)
    #print(a)
    return tree

def getMatrixByTime(docsOfThemesOrdened, topicsSumary, datesThemes):
    lenMuesta = len(docsOfThemesOrdened)
    dis_matrix = numpy.zeros((lenMuesta, lenMuesta))
    min_date = min(datesThemes)
    max_date = max(datesThemes)

    k = 1000

    for v1 in range(0, lenMuesta):
        for v2 in range(0, lenMuesta):
            if v1 == v2:
                dis_matrix[v1][v2] = 0
            if v1 < v2:
                date1 = topicsSumary[v1][2]
                date2 = topicsSumary[v2][2]

                if (date1-min_date) > (date2-min_date):
                    dist_temp = 1 - math.exp(-((date1-min_date)*360/k))#(dates[i]-min_date).days
                    dis_matrix[v1][v2] = dist_temp
                    dis_matrix[v2][v1] = dist_temp
                else:
                    dist_temp = 1 - math.exp(-((date2-min_date)*360/k))#(dates[j]-min_date).days
                    dis_matrix[v1][v2] = dist_temp
                    dis_matrix[v2][v1] = dist_temp

    return dis_matrix

def getTopDocsOfThemesOrdened(docsOfThemesOrdened):
    docsOfThemesOrdenedTop = []
    for theme in docsOfThemesOrdened:
        themeTop = []
        for i in range(0, len(theme)):
            if theme[i] > 0.001:
                themeTop.append(theme[i])
        docsOfThemesOrdenedTop.append(themeTop)
    return docsOfThemesOrdenedTop

def getMeta(pubmed, pmidToId, idToPmid, docsDescript, topicsSumary, docsOfThemesOrdened, nameThemes, idDocOrdened, datesDoc):
    metaDoc = {"pubmed": pubmed, "pmidToId": pmidToId,
               "idToPmid": idToPmid, "distributionDoc": docsDescript, "idDocOrdened": idDocOrdened, "datesDoc": datesDoc
               }
    metaTheme = {"topicsSumary": topicsSumary, "distributionThemes": docsOfThemesOrdened,  #themesDescriptTopOrd, #themesDescript,
                 "nameThemes": nameThemes#, "idThemeOrdened": idThemeOrdened, "datesThemes": datesThemes,
                 }
    return metaDoc, metaTheme

def getNameThemes(themesDescript):
    nameThemes = []
    for theme in range(0, len(themesDescript)):
        nameThemes.append("theme_"+str(theme))
    return nameThemes

def normalize_matrix(m_c, m_t):
    max_val_m_cont = m_c.max()
    max_val_m_t = m_t.max()
    #max_val = max(max_val_m_cont, max_val_m_t)

    for f in range(0, len(m_c)):
        for c in range(0, len(m_c)):
            m_c[f, c] = m_c[f, c] / max_val_m_cont
            m_t[f, c] = m_t[f, c] / max_val_m_t
    return m_c, m_t

def njByDoc(pubmed, themesDescript, idToPmid, metaDoc, metaTheme, venue_to_color):
    allDocThemeTop = []
    jsonNJinThemes = {}
    cont_theme = 0
    for theme in themesDescript:
        docThemeTop = {}
        for i in range(0, len(theme)):
            if theme[i] > 0.001:
                docThemeTop[idToPmid[i]] = pubmed.docs[idToPmid[i]]
        allDocThemeTop.append(docThemeTop)

        DicTextDocs = getTexOfDocs(docThemeTop) # puede que el se filtre por ejemplo  50 documentos pero entre ellos habra algunos que no tienen informacion ni de titulo ni de abstrar ni de cuerpo, esos tambien son eliminados
        idListTextDocs, listTextDocs = convertToList(DicTextDocs)
        print("Get Matrix")
        m = get_matrix(listTextDocs)
        #m = numpy.matrix(m)
        t = njWithRoot(m, idListTextDocs)
        rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
        radialLayout(rootedTree)
        jsonTree = treeToJsonPubmedDoc(rootedTree, metaDoc, metaTheme, venue_to_color)
        jsonNJinThemes["theme_" + str(cont_theme)] = jsonTree
        cont_theme = cont_theme + 1
    return jsonNJinThemes


def generateJsonbyClustering(file_lda, result_name):
    pubmed = getPubMedCorpus()  # load raw data
    #print(pubmed.docs[21172003])
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pubmed)
    ldaFilePath = os.path.join(variables.TEST_RESULT, file_lda+'.lda')
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath)  # load lda result
    ldaTopicSumaryFilePath = os.path.join(variables.TEST_RESULT, file_lda+'.lda_summary')
    topicsSumary = readTopicSummary(ldaTopicSumaryFilePath)  # load lda sumary for order descriptor by time

    # we get characteristic description of each document, this was calculated by lda before
    # the detail is that descriptor is in disorder
    docsDescript = ldaInstance.thetaEstimate  # the descriptor of each document is conformed by a set of themes
    themesDescript = ldaInstance.phiEstimate  # the descriptor of each themes is conformed by a set of citation

    (idThemeOrdened, datesThemes) = getIdAndDatesOfThemesOrdered(topicsSumary)  # idThemeOrdened are ids that are ordened by time and dataThemes are dates ordened by time
    (idDocOrdened, datesDoc) = getIdAndDatesOfDocOrdered(ldaInstance, pubmed, idToPmid)
    docsOfThemesOrdened = getDocOfThemesOrdered(idDocOrdened, themesDescript)
    docsOfThemesOrdenedTop = getTopDocsOfThemesOrdened(docsOfThemesOrdened)

    #rootedTree, metaDoc, metaTheme = njByTheme(docsOfThemesOrdenedTop, docsOfThemesOrdened, topicsSumary, datesThemes, themesDescript, pmidToId, idToPmid, docsDescript, idDocOrdened, datesDoc)

    #dis_matrix = numpy.multiply(dis_matrix, dis_matrix) #para incrementar cada valor al doble

    #a = numpy.asarray(dis_matrix)
    #numpy.savetxt("dis_matrix.csv", a, delimiter=",")
    #print('generate image of document')
    #generateImageDistribution(docsThemesOrdened, datesThemes, list(idToPmid.values()))  # muestraPmid generate image about themes' distribution of each document

    #print('generate image of themes')
    # None pues en el caso de los temas solo es necesario las coordenadas del eje y
    #generateImageDistribution(themesDescript, None, [i for i in range(0, len(themesDescript))])  # muestraPmid generate image about themes' distribution of each document
    nameThemes = getNameThemes(themesDescript)
    metaDoc, metaTheme = getMeta(pubmed, pmidToId, idToPmid, docsDescript, topicsSumary, docsOfThemesOrdened, nameThemes, idDocOrdened, datesDoc)
    venue_to_color = {"BMC_Bioinformatics": "red", "Crit_Care": "Yellow", "Evid_Based_Complement_Alternat_Med": "Lime", "Genome_Biol": "Green", "J_Cell_Biol": "Aqua", "J_Exp_Med": "Purple", "J_Gen_Physiol": "Blue", "Malar_J": "Fuchsia", "Nucleic_Acids_Res": "Teal","Environ_Health_Perspect": "silver", "Diabetes_Care": "maroon"}


    allJsonDocThemeTop = njByDoc(pubmed, themesDescript, idToPmid, metaDoc, metaTheme, venue_to_color)

    #print('save result pex format')
    #res = matrix_to_pex('matrix_of_docs', dis_matrix, muestraPmid)
    print('calculate matrix distance')
    dis_matrix_cont = getMatrixDist(docsOfThemesOrdenedTop, fastdtw)  # for themes dist_cosine(docsOfThemesOrdened) fastdtw (docsOfThemesOrdenedTop) dist_euclidean (docsOfThemesOrdened) hellinger(docsOfThemesOrdened)
    #dis_matrix_time = getMatrixByTime(docsOfThemesOrdened, topicsSumary, datesThemes)

    #dis_mCont_norm , dis_mTime_norm = normalize_matrix(dis_matrix_cont, dis_matrix_time)

    #dis_matrix = (numpy.matrix(dis_mCont_norm) + numpy.matrix(dis_mTime_norm))/2
    # método para aplicar nj y ademas calcula la raiz, mejor dicho lo convierte en un árbol con raiz
    
    t = njWithRoot(dis_matrix_cont, nameThemes)  # for themes / dis_matrix

    rootedTree = EteTreeToBinaryTree(t)  # since now, we use only themes
    radialLayout(rootedTree)

    jsonTree = treeToJsonPubmed(rootedTree, metaDoc, metaTheme, venue_to_color, allJsonDocThemeTop)

    #name_result = "C:/Users/rbrto-pc/Google Drive/citation_lda/src/clustering_process/final_result/"+file_lda+"_only_content.json"
    path_res = "D:/Google Drive/citation_lda/src/clustering_process/final_result/"
    jsonfile = open(path_res+result_name, 'w')
    #print(jsonTree)
    jsonfile.write(jsonTree)
    #print("hello word")

if __name__ == '__main__':
    file_lda = 'pubmed_citation_lda_45_27991_27991_0.001_0.001_timeCtrl_3_4.5'
    generateJsonbyClustering(file_lda)
