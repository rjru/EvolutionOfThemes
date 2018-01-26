from toolkit import variables
from corpus.pubmed import PubMed
from deep_nlp.text import wordTokenize;
from nltk import *
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

def getTexOfDocs(docs): #extrae el texto que viene a ser el title + abstract + body
    dictTextDoc = {}
    for doc in docs:
        aux = '' if 'title' not in docs[doc] else docs[doc]['title'] + '' if 'abstract' not in docs[doc] else docs[doc]['abstract'] + '' if 'body' not in docs[doc] else docs[doc]['body']
        if aux != "":
            dictTextDoc[doc] = aux

    return dictTextDoc;

def getTokenTexOftDocs(DicTextDocs):
    dictTokenTextDoc = {}
    for doc in DicTextDocs:
        dictTokenTextDoc[doc] = wordTokenize(DicTextDocs[doc], stemmingOption=True, rmStopwordsOption=True);
        #print(docs[doc]['abstract'])
    return dictTokenTextDoc;

def getCountTokDocs(DicTokenTextDocs, top):
    countTokDocs = {}
    for doc in DicTokenTextDocs:
        #countTokDocs[doc] = Counter(DicTokenTextDocs[doc])
        fdist = FreqDist(ch.lower() for ch in DicTokenTextDocs[doc] if ch.isalpha())
        countTokDocs[doc] =fdist.most_common(top)
        #print(fdist.most_common(5))
        #print(docs[doc]['abstract'])
    return countTokDocs;

def SaveCountTokDocs(DicTokenTextDocs, name_file):
    file = open(name_file+'.csv', "w")
    for doc in DicTokenTextDocs:
        row = str(doc)
        for tok in DicTokenTextDocs[doc]:
            row = row + "; " + str(tok)
        file.write(row+"\n")

def saveFreqTokDocs(name, FreqTokDocs):
    filehandler = open(name+'.data', 'wb')
    pickle.dump(FreqTokDocs, filehandler)
    #with open("C:/Users/rbrto-pc/Google Drive/citation_lda/src/clustering_process/variable_FreqTokDocs", 'rb') as pickle_file:
    #    content = pickle.load(pickle_file)
    SaveCountTokDocs(FreqTokDocs, name)

# propio procesamiento TF IDF
token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def get_matrix(contentDocs):
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english', max_features=200,  encoding='utf-8', decode_error='replace')
    tfs = tfidf.fit_transform(contentDocs)

    print("tfidf.fit_transform")
    filehandler = open('vector.tfidf', 'wb')
    pickle.dump(tfs, filehandler)

    m = open('vectorcosine.csv', 'w')

    for a in tfs:
        for b in tfs:
            cs = cosine_similarity(a, b)
            w = str(abs((cs - 1).round(8))[0][0])+";"
            m.write(w)
        m.write("\n")

    res_matrix1 = cosine_similarity(tfs, tfs, dense_output=True)

    #print("cosine simlilarity sin round")
    #filehandler = open('vector.cosine', 'wb')
    #pickle.dump(res_matrix, filehandler)

    res_matrix = abs(res_matrix1.round(8) - 1)  # .todense()

    return res_matrix

def convertToList(DicTextDocs):
    id = []
    text = []
    for doc in DicTextDocs:
        id.append(doc)
        text.append(DicTextDocs[doc])
    return id, text

if (__name__ == '__main__'):
    metaDataFilePath = os.path.join(variables.TEST_ROOT_N, 'pubmed_metadata.txt');
    citFilePath = os.path.join(variables.TEST_ROOT_N, 'pubmed_citation.txt');
    absFilePath = os.path.join(variables.TEST_ROOT_N, 'pubmed_abstract.txt');
    bodyFilePath = os.path.join(variables.TEST_ROOT_N, 'pubmed_body.txt');

    print("Get document")
    muestra_docs = {}
    pubmed = PubMed(metaDataFilePath, None, absFilePath, bodyFilePath);
    docsss = pubmed.docs

    c = 0
    for d in docsss:
        if c == 5:
            break
        else:
            muestra_docs[d] = docsss[d]
        c = c + 1


    print("Get text of docs")
    #muestra doc: es un diccionario con el pmid y los datos de cada paper
    DicTextDocs = getTexOfDocs(muestra_docs)
    idListTextDocs, listTextDocs = convertToList(DicTextDocs)
    print("Get Matrix")
    m = get_matrix(listTextDocs)
    #print("Matrix save")
    #filehandler = open('m.matrix', 'wb')
    #pickle.dump(m, filehandler)
    #print("hola")

    #print("Get token of Docs")
    #DicTokenTextDocs = getTokenTexOftDocs(DicTextDocs)
    #print("Frecuency of docs")
    #FreqTokDocs = getCountTokDocs(DicTokenTextDocs, 20)
    #saveFreqTokDocs('fileFreqTokDocs', FreqTokDocs)
    #all_tokens_set = set([item for sublist in FreqTokDocs for item in sublist])
    #print(FreqTokDocs)
    #print(all_tokens_set)