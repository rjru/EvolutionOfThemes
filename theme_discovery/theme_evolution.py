'''
Created on Feb 16, 2013

@author: xwang95
'''
import theme_discovery.citation_based_method;
import toolkit.variables;
import toolkit.utility;
import os.path;
import random;
import corpus.pubmed;
import toolkit.gexf;
import math;

def getMatrixDominantEigenVec(m):
    v = [random.random() for i in range(len(m))];
    iter = 0;
    while(True):
        v = toolkit.utility.normalizeVector(v);
        v_new = toolkit.utility.getMatrixVecMultiply(m, v);
        if(toolkit.utility.getVecNorm(toolkit.utility.getVecSubstract(v, v_new), 2) < 1e-6): break;
        v = v_new;
        iter += 1;
    print(iter);
    return v;

def getTopicCitationProb(citMatrix, topicSummaryDict, pmd):
    topicStationaryProbLst = getMatrixDominantEigenVec(toolkit.utility.getTransposeSquareMatrix(citMatrix));
    topicNum = len(citMatrix);
    forwardProb = 0.0;
    backwardProb = 0.0;
    selfProb = 0.0;
    for k1 in range(topicNum):
        for k2 in range(topicNum):
            if(topicSummaryDict[k1][2] < topicSummaryDict[k2][2]): forwardProb += topicStationaryProbLst[k1] * citMatrix[k1][k2];
            elif(k1 == k2): selfProb += topicStationaryProbLst[k1] * citMatrix[k1][k2];
            else: backwardProb += topicStationaryProbLst[k1] * citMatrix[k1][k2];
    print('[Topic Citation Probability]: backward_prob = {0}'.format(backwardProb));
    print('[Topic Citation Probability]: forward_prob  = {0}'.format(forwardProb));
    print('[Topic Citation Probability]: self_prob     = {0}'.format(selfProb));
    deltaYrDistDict = {};
    for citingPmid in pmd.citMetaGraph:
        for citedPmid in pmd.citMetaGraph[citingPmid]:
            deltaYr = pmd.docs[citingPmid]['year'] - pmd.docs[citedPmid]['year'];
            if(deltaYr > 300):
                print (citingPmid, pmd.docs[citingPmid]['year'])
                print (citedPmid, pmd.docs[citedPmid]['year'])
            deltaYrDistDict[deltaYr] = deltaYrDistDict.get(deltaYr, 0.0) + pmd.citMetaGraph[citingPmid][citedPmid];
    print('[Topic Citation Probability]: delta year dist');
    for deltaYr in sorted(deltaYrDistDict):
        print (deltaYr, deltaYrDistDict[deltaYr]);
    return;

def getVenueRanking(topicSummaryDict):
    vensDict = {};
    for topicId in range(len(topicSummaryDict)):
        (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens) = topicSummaryDict[topicId];
        for (prob, ven) in topVens:
            vensDict[ven] = vensDict.get(ven, 0.0) + topicProb * prob;
    return vensDict;
        

def getVenueEntropy(topicSummaryDict):
    venEnt = 0.0;
    for topicId in range(len(topicSummaryDict)):
        remProb = 1.0;
        minProb = 1.0;
        (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens) = topicSummaryDict[topicId];
        for (prob, ven) in topVens: 
            venEnt += -topicProb * prob * math.log(prob);
            remProb -= prob;
            minProb = min(minProb, prob);
        venEnt += -topicProb * remProb * math.log(minProb);
    topicEnt = 0.0;
    for topicId in range(len(topicSummaryDict)): topicEnt += -topicProb * math.log(topicProb);
    return (venEnt, topicEnt, topicEnt + venEnt);
             
NOT_FOLD = True;    
# def graphFilter(citMatrix, topicSummaryDict):
#    
#    return;
#===============================================================================
# API
#===============================================================================
def dumpGraphFile(citMatrixFilePath, topicSummaryFilePath, edgeWeightThreshold, noSingleton=True, noBackwardEdge=True):
    citMatrix = theme_discovery.citation_based_method.readCitMatrixSummary(citMatrixFilePath);
    topicSummaryDict = theme_discovery.citation_based_method.readTopicSummary(topicSummaryFilePath);
#    (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens)
    gexfFilePath = citMatrixFilePath.replace("_citMatrix", ".gexf");
    gexfGen = toolkit.gexf.GexfGen();
    topicIdToTimeSortedId = {};
    for topicId in sorted(topicSummaryDict, key=lambda x: topicSummaryDict[x][2]): topicIdToTimeSortedId[topicId] = len(topicIdToTimeSortedId);
    validNodeSet = set();
    for i in range(len(topicSummaryDict)):
        for j in range(len(topicSummaryDict)):
            if(i != j and citMatrix[i][j] >= edgeWeightThreshold): 
                if(noBackwardEdge and topicIdToTimeSortedId[i] > topicIdToTimeSortedId[j]):
                    validNodeSet.add(i); 
                    validNodeSet.add(j);    
    for topicId in range(len(topicSummaryDict)):
        if(noSingleton and (topicId not in validNodeSet)): continue;
        (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens) = topicSummaryDict[topicId];
        gexfGen.addNodeAtt(topicIdToTimeSortedId[topicId], 'topicId', topicId, 'integer');
        gexfGen.addNodeAtt(topicIdToTimeSortedId[topicId], 'timeSorted', topicIdToTimeSortedId[topicId], 'integer');
        gexfGen.addNodeAtt(topicIdToTimeSortedId[topicId], 'year', topicYearMean, 'double');
        gexfGen.addNodeAtt(topicIdToTimeSortedId[topicId], 'prob', topicProb, 'double');
    edgeNum = 0;
    for i in range(len(topicSummaryDict)):
        for j in range(len(topicSummaryDict)):
            if(i != j):
                if(citMatrix[i][j] >= edgeWeightThreshold):
                    if(noBackwardEdge and topicIdToTimeSortedId[i] > topicIdToTimeSortedId[j]):
                        gexfGen.addEdge(topicIdToTimeSortedId[i], topicIdToTimeSortedId[j], citMatrix[i][j]);
                        edgeNum += 1;
    print('[dump graph file]: {0} edges'.format(edgeNum));
    graphStr = gexfGen.getGraphStr();
    gexfFile = open(gexfFilePath, 'w');
    gexfFile.write(graphStr);
    gexfFile.close();
    return;

def dumpVenRankingFile(topicSummaryFilePath):
    vensDictFilePath = topicSummaryFilePath.replace('_summary', '_venDict');
    vensDictFile = open(vensDictFilePath, 'w');
    topicSummaryDict = theme_discovery.citation_based_method.readTopicSummary(topicSummaryFilePath);
    vensDict = getVenueRanking(topicSummaryDict);
    for ven in sorted(vensDict, key=lambda x:vensDict[x], reverse=True):
        vensDictFile.write('[{0:.6f}]: {1}\n'.format(vensDict[ven], ven));
    vensDictFile.close();

def printVenEntropy(topicSummaryFilePath):
    topicSummaryDict = theme_discovery.citation_based_method.readTopicSummary(topicSummaryFilePath);
    print (getVenueEntropy(topicSummaryDict));



if(__name__ == "__main__"):
    citMatrixFilePath = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_citMatrix_timeSorted');
    #topicSummaryFilePath1 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda', 'pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_10_10.lda_summary');
    #topicSummaryFilePath2 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda', 'pubmed_citation_lda_100_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary');
    topicSummaryFilePath2 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary');

    #citMatrixFilePath = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda', 'pubmed_citation_lda_100_145317_145317_0.001_0.001_timeCtrl_30_45.lda_citMatrix');
    topicSummaryFilePath = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary');
    citMatrix = theme_discovery.citation_based_method.readCitMatrixSummary(citMatrixFilePath);
    topicSummaryDict = theme_discovery.citation_based_method.readTopicSummary(topicSummaryFilePath);
#    pmd = corpus.pubmed.getPubMedCorpus();
    
#    getTopicCitationProb(citMatrix, topicSummaryDict, pmd);
    
    edgeWeightThreshold = 0.02;
    dumpGraphFile(citMatrixFilePath, topicSummaryFilePath, edgeWeightThreshold);
#    dumpVenRankingFile(topicSummaryFilePath);
    #printVenEntropy(topicSummaryFilePath1);
    printVenEntropy(topicSummaryFilePath2);
    #topicSummaryFilePath3 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_content_title_lda', 'pubmed_content_title_lda_500_317975_22312_0.001_0.001_timeCtrl_12_12.lda_summary');
    #topicSummaryFilePath4 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_content_title_lda', 'pubmed_content_title_lda_100_317975_22312_0.001_0.001_timeCtrl_12_12.lda_summary');        
    #printVenEntropy(topicSummaryFilePath3);
    
    #printVenEntropy(topicSummaryFilePath4);
    pass;