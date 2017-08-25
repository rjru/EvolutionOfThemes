# -*- coding: utf-8 -*-
'''

aqui se trató de obtener descriptores de catacteristicas a partir del titulo abastract y body,  para luego sacar
un descriptor de caracteristicas de temas de cada documento, esta forma es inadecuada solo conservare los metodos hechos
a parte el mismo LDA genera la probabilidad

'''
from toolkit import utility, variables
import os.path;
from corpus.pubmed import PubMed
from deep_nlp.text import wordTokenize;
from theme_discovery.citation_based_method import readTopicSummary
from collections import Counter

def getTexOfDocs(docs): #extrae el texto que viene a ser el title + abstract + body
    dictTextDoc = {}
    for doc in docs:
        dictTextDoc[doc] = docs[doc]['title'] + docs[doc]['abstract'] + docs[doc]['body']
        #print(docs[doc]['abstract'])
    return dictTextDoc;

def getTokenTexOftDocs(DicTextDocs):
    dictTokenTextDoc = {}
    for doc in DicTextDocs:
        dictTokenTextDoc[doc] = wordTokenize(DicTextDocs[doc], stemmingOption=True, rmStopwordsOption=True);
        #print(docs[doc]['abstract'])
    return dictTokenTextDoc;

def getCountTokDocs(DicTokenTextDocs):
    countTokDocs = {}
    for doc in DicTokenTextDocs:
        countTokDocs[doc] = Counter(DicTokenTextDocs[doc])
        #print(docs[doc]['abstract'])
    return countTokDocs;  

def getProbDocInTopic(lstTokDoc, lstTokTop):
    #lstTokDocExample = CountTokDocs[18391373]
    #lstTokTopExample = topicsSumary[0][5]
    #cont = 0    
    prob = 0
    for tokTop in lstTokTop:
        #print(tokTop[1])
        for tokDoc in lstTokDoc:
            #print(tokDoc)
            if(tokTop[1] == tokDoc):
                # ocurrencia de la palabra en el doc: lstTokDocExample[tokDoc] * la probabilidad de la palabra en el tema: tokTop[1]
                #print(lstTokDoc[tokDoc])
                #print(tokTop[0])
                prob = lstTokDoc[tokDoc] * tokTop[0] + prob
                #cont = cont + 1
                #print(tokDoc)
    #vectorDocThemes[]
    return(prob)

def getvectorDocsThemes(CountTokDocs, topicsSumary):
    # get vector characteristic conformed by themes
    vectorDocsThemes = {}
    for LstTokDoc in CountTokDocs:# recorremos el dict de docs 
        vectorDocThemes = {}
        for topic in topicsSumary:
            #print(type(topicsSumary[topic][5]))
            #lstTokTopic = topicsSumary[topic][5]
            vectorDocThemes[topic] = {'prob':getProbDocInTopic(CountTokDocs[LstTokDoc], topicsSumary[topic][5]),'date':topicsSumary[topic][2]}
        vectorDocsThemes[LstTokDoc] = vectorDocThemes
    
    return vectorDocsThemes

if(__name__ == '__main__'): 
    
    metaDataFilePath = os.path.join(variables.DATA_DIR, 'PubMed/pubmed_metadata.txt');
    citFilePath = os.path.join(variables.DATA_DIR, 'PubMed/pubmed_citation.txt');
    absFilePath = os.path.join(variables.DATA_DIR, 'PubMed/pubmed_abstract.txt');
    bodyFilePath = os.path.join(variables.DATA_DIR, 'PubMed/pubmed_body.txt');
    
    pubmed = PubMed(metaDataFilePath, None, absFilePath, bodyFilePath);
    docsss = pubmed.docs
    DicTextDocs = getTexOfDocs(pubmed.docs)
    DicTokenTextDocs = getTokenTexOftDocs(DicTextDocs)
    CountTokDocs = getCountTokDocs(DicTokenTextDocs)
    
    ldaTopicSumaryFilePath = 'C:/Users/rbrto/Documents/citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary';
    topicsSumary = readTopicSummary(ldaTopicSumaryFilePath)
    
        
    vectorDocsThemes = getvectorDocsThemes(CountTokDocs, topicsSumary)
    
    #lstProb = []
#    for k in sorted(vectorDocsThemes[18391392], key=lambda k:vectorDocsThemes[18391392][k]['date']):
#        #print(k,", ",vectorDocsThemes[18391373][k]['date'])
#        print(vectorDocsThemes[18391392][k]['date'], ";", vectorDocsThemes[18391392][k]['prob'])
#        #lstProb.append(vectorDocsThemes[18391373][k]['prob'])
#    #for k in sorted(topicSummaryDict, key=lambda k:topicSummaryDict[k][2]):

#lstTokDocExample = CountTokDocs[18391373]
#lstTokTopExample = topicsSumary[0][5]       
#reee = getProbDocInTopic(lstTokDocExample, lstTokTopExample)


    fv = open('fileToVis.csv', 'w')
    # escribimos el encabezado
    listId = list(vectorDocsThemes)
    fv.write("date, "+str(listId).strip("[]")+"\n")
    for k in sorted(topicsSumary, key=lambda k:topicsSumary[k][2]):
        valuesOfDoc = ""
        for docId in listId:
            if valuesOfDoc == "":
                valuesOfDoc = valuesOfDoc + str(vectorDocsThemes[docId][k]['prob'])
            else:
                valuesOfDoc = valuesOfDoc +", "+str(vectorDocsThemes[docId][k]['prob'])
                    
        fv.write(str(topicsSumary[k][2])+", "+valuesOfDoc+"\n")
    fv.close()
        

    


           
            
    
    

    
    

    
    
    
    
    
    

