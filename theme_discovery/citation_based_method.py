'''
Created on Feb 5, 2013

@author: xwang95
'''
import corpus.pubmed;
import toolkit.utility;
import topic_modeling.lda;
import os.path;
import deep_nlp.text;
import sys;
from toolkit import variables;
from corpus.pubmed import getPubMedCorpus, getCitMetaGraphPmidIdMapping, getCitMetaGraphDocWrdCntTupleLst;
import re;
from toolkit.utility import parseNumVal
from toolkit import utility

def citationLdaRun(data, K, D, W, alpha, beta, burninTimeHr, sampliTimeHr, dumpFileFolder):
                                                                                        #   pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45
                                                                                        # K = 500, D = 145317, W = 145317, alpha = 0.001, beta = 0.001, burninTimeHr = 30, sampliTimeHr = 45
                                                                                        # K: number of topics, D: total number of document, alpha and beta: default values,
                                                                                        #
    dumpFilePath = os.path.join(dumpFileFolder, 'pubmed_citation_lda_{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}.lda'.format(K, D, W, alpha, beta, 'timeCtrl', burninTimeHr, sampliTimeHr));
    toolkit.utility.removePath(dumpFilePath);
    # inicializalización de la instancia lda
    ldaInstance = topic_modeling.lda.LDA(data, K, D, W, alpha, beta, burnTime=burninTimeHr, sampTime=sampliTimeHr, iterCtrl=False);
    (postTheta, postPhi, topicWeights) = ldaInstance.Mcmc();
    topic_modeling.lda.dumpLdaEstimateFile(ldaInstance, dumpFilePath)
    return (postTheta, postPhi, topicWeights);

def getCitationMatrix(ldaInstance):
    print('[citation matrix]: computing citation matrix');
    thetaMatrix = ldaInstance.thetaEstimate;
    phiMatrix = ldaInstance.phiEstimate;
    topicWeightVec = ldaInstance.topWeiEstimate;
    citMatrix = [[0.0 for k1 in range(ldaInstance.K)] for k2 in range(ldaInstance.K)];
    #===========================================================================
    # P(c2 | c1) = sum_d phi_c1(d) theta_d(c2)
    #===========================================================================
    cnt = 0;
    for d in range(ldaInstance.D):
        k1Lst = [k for k in range(ldaInstance.K) if phiMatrix[k][d] != 0.0];
        k2Lst = [k for k in range(ldaInstance.K) if thetaMatrix[d][k] != 0.0];
        for k1 in k1Lst:
            for k2 in k2Lst:
                citMatrix[k1][k2] += phiMatrix[k1][d] * thetaMatrix[d][k2];
        if(d % 10 == 0): toolkit.utility.printProgressBar(float(d) / ldaInstance.D);
    print('');
    return citMatrix;

def filterTokLst(tokLst): return [tok for tok in tokLst if (len(tok) > 1)];

def getTopicSummary(pmd, pmidToId, idToPmid, ldaInstance, topDocCnt=20, topTokCnt=20, topVenueCnt=20):
    phiMatrix = ldaInstance.phiEstimate;
    topWeiVec = ldaInstance.topWeiEstimate;
    topicSummary = {};
    for k in range(ldaInstance.K):
        sys.stdout.write('\r[topic summary]: process topic {0}'.format(k));
        sys.stdout.flush();
        tokExptFreq = {};
        venueDist = {};
        yearDist = {};
        topDocs = [];
        topToks = [];
        for d in range(ldaInstance.D):
            prob = phiMatrix[k][d];
            pmid = idToPmid[d];
            title = pmd.docs[pmid]['title'];
            venue = pmd.docs[pmid]['venue'];
            year = pmd.docs[pmid]['year'];
            tokLst = filterTokLst(deep_nlp.text.wordTokenize(title, rmStopwordsOption=True)); 
            for tok in tokLst: tokExptFreq[tok] = tokExptFreq.get(tok, 0.0) + prob;
            venueDist[venue] = venueDist.get(venue, 0.0) + prob;
            yearDist[year] = yearDist.get(year, 0.0) + prob;
        topDocId = [d for d in sorted(range(ldaInstance.D), key=lambda x:phiMatrix[k][x], reverse=True)][0:topDocCnt];
        topDocs = [(phiMatrix[k][d], pmd.docs[idToPmid[d]]['venue'], pmd.docs[idToPmid[d]]['title']) for d in topDocId];
        topTokId = [t for t in sorted(tokExptFreq, key=lambda x:tokExptFreq[x], reverse=True)][0:topTokCnt];
        topToks = [(tokExptFreq[tok], tok) for tok in topTokId];
        topVenueId = [venue for venue in sorted(venueDist, key=lambda x:venueDist[x], reverse=True)][0:topVenueCnt];
        topVenues = [(venueDist[venue], venue) for venue in topVenueId];
        topicSummary[k] = (topToks, venueDist, yearDist, topWeiVec[k], topDocs, topVenues);
    print('');           
    return topicSummary;

def dumpTopicSummary(topicSummary, dumpFilePath):
    print('[topic summary]: dump to file {0}'.format(dumpFilePath));
    dumpFile = open(dumpFilePath, 'w');
    for k in sorted(topicSummary, key=lambda k:topicSummary[k][3], reverse=True):
        sys.stdout.write('\r[topic summary]: dump topic {0}'.format(k));
        sys.stdout.flush();
        (topToks, venueDist, yearDist, topWei, topDocs, topVenues) = topicSummary[k];
        dumpFile.write('[Topic: {0}]:{1:.6f}  year={2:.6f}({3:.6f})\n'.format(k, topWei, toolkit.utility.getDistExpectation(yearDist), toolkit.utility.getDistStd(yearDist)));
        for topDoc in topDocs: dumpFile.write('Doc:{0:.6f}:[{1:^20}]:{2}\n'.format(topDoc[0], topDoc[1], topDoc[2]));
        for topTok in topToks: dumpFile.write('Tok:{0:.6f}:{1}\n'.format(topTok[0], topTok[1]));
        for topVenue in topVenues: dumpFile.write('Ven:{0:.6f}:{1}\n'.format(topVenue[0], topVenue[1]));
        dumpFile.write('\n');
    print('');
    dumpFile.close();
    
def dumpShortTopicSummary(topicSummary, dumpFilePath):
    print('[topic short summary]: dump to file {0}'.format(dumpFilePath));
    dumpFile = open(dumpFilePath, 'w');
    for k in sorted(topicSummary, key=lambda k:topicSummary[k][3], reverse=True):
        sys.stdout.write('\r[topic short summary]: dump topic {0}'.format(k));
        sys.stdout.flush();
        (topToks, venueDist, yearDist, topWei, topDocs, topVenues) = topicSummary[k];
        dumpFile.write('[Topic: {0}]:{1:.6f}  year={2:.2f}({3:.2f}) '.format(k, topWei, toolkit.utility.getDistExpectation(yearDist), toolkit.utility.getDistStd(yearDist)));
        for topTok in topToks: dumpFile.write('{0} '.format(topTok[1]));
        dumpFile.write('\n');
    print('');
    dumpFile.close();
        
def readTopicSummary(topicSummaryFilePath):
    topicLnRe = re.compile(r'\[Topic: (.*?)\]:(.*?)  year=(.*?)\((.*?)\)');
    docLnRe = re.compile(r'Doc:(.*?):[(.*?)]:(.*)');
    tokLnRe = re.compile(r'Tok:(.*?):(.*)');
    venLnRe = re.compile(r'Ven:(.*?):(.*)');
    topicSummaryDict = {};
    topicSummaryFile = open(topicSummaryFilePath, 'r');
    eof = False;
    while(not eof):
        (chunkLnLst, eof) = toolkit.utility.readChunk(topicSummaryFile);
        topicId = None;
        topicProb = None;
        topicYearMean = None;
        topicYearVar = None;
        topDocs = [];
        topToks = [];
        topVens = [];
        for ln in chunkLnLst:
            topicLnReMatch = topicLnRe.match(ln);
            if(topicLnReMatch):
                topicId = toolkit.utility.parseNumVal(topicLnReMatch.group(1));
                topicProb = toolkit.utility.parseNumVal(topicLnReMatch.group(2));
                topicYearMean = toolkit.utility.parseNumVal(topicLnReMatch.group(3));
                topicYearVar = toolkit.utility.parseNumVal(topicLnReMatch.group(4));
                continue;
            docLnReMatch = docLnRe.match(ln);
            if(docLnReMatch):
                docProb = toolkit.utility.parseNumVal(docLnReMatch.group(1));
                docVen = docLnReMatch.group(2).strip();
                docTitle = docLnReMatch.group(3).strip();
                topDocs.append((docProb, docVen, docTitle));
                continue;
            tokLnReMatch = tokLnRe.match(ln);
            if(tokLnReMatch):
                tokProb = toolkit.utility.parseNumVal(tokLnReMatch.group(1));
                tok = tokLnReMatch.group(2).strip();
                topToks.append((tokProb, tok));
                continue;
            venLnReMatch = venLnRe.match(ln);
            if(venLnReMatch):
                venProb = toolkit.utility.parseNumVal(venLnReMatch.group(1));
                ven = venLnReMatch.group(2).strip();
                topVens.append((venProb, ven));
                continue;
        if(topicId is not None): topicSummaryDict[topicId] = (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens);
    return topicSummaryDict;

def readCitMatrixSummary(citMatrixFilePath):
    citMatrixFile = open(citMatrixFilePath, 'r');
    (citMatrix, eof) = toolkit.utility.readMatrix(citMatrixFile);
    return citMatrix;
    
NOT_FOLD = True;
#===============================================================================
# MAIN
#===============================================================================
def pubmedCitationLdaRun(K, BurninHr, SampliHr): # metodo principal para extraer lda citation de pubmed
    #dumpFileFolder = os.path.join(variables.RESULT_DIR, 'pubmed_citation_lda/');
    dumpFileFolder = variables.TEST_RESULT;
    '''data loading'''
    print('[pubmed-citation-LDA]: loading pubmed');
    pmd = getPubMedCorpus(); # retorna cargada la bd de pubmed metadata, citas y abstract
    print('[pubmed-citation-LDA]: indexing');
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pmd); # matriz de citas
    D = len(pmidToId);
    print('                       size: {0}'.format(D));
    print('[pubmed-citation-LDA]: insert tuple (doc, wrd, cnt) to list');
    data = getCitMetaGraphDocWrdCntTupleLst(pmd, pmidToId, idToPmid);
    print('                       size: {0}'.format(len(data)));
    '''running LDA'''
    (postTheta, postPhi, topicWeights) = citationLdaRun(data, K, D, D, 0.001, 0.001, BurninHr, SampliHr, dumpFileFolder);
    return;

def pubmedCitationLdaSummary(ldaFilePath):
    print('[pubmed-citation-LDA]: loading lda');
#    ldaFilePath = os.path.join(variables.RESULT_DIR, 'pubmed_citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_10_10.lda');
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath);
    print('[pubmed-citation-LDA]: loading pubmed');
    pmd = getPubMedCorpus();
    print('[pubmed-citation-LDA]: indexing');
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pmd);
    venueNum = pmd.getVenueNum(pmidToId.keys());
    print('[pubmed-citation-LDA]: venue number {0}'.format(venueNum));
    print('[pubmed-citation-LDA]: topic summary generation');
    topicSummary = getTopicSummary(pmd, pmidToId, idToPmid, ldaInstance, topDocCnt=10, topTokCnt=20);
    print('[pubmed-citation-LDA]: topic summary dump');
    dumpTopicSummary(topicSummary, ldaFilePath + '_summary');
    dumpShortTopicSummary(topicSummary, ldaFilePath + '_shortsummary');
    return;

def pubmedCitationLdaShortSummary(ldaFilePath):
    print('[pubmed-citation-LDA]: loading lda');
#    ldaFilePath = os.path.join(variables.RESULT_DIR, 'pubmed_citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_10_10.lda');
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath);
    print('[pubmed-citation-LDA]: loading pubmed');
    pmd = getPubMedCorpus();
    print('[pubmed-citation-LDA]: indexing');
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pmd);
    venueNum = pmd.getVenueNum(pmidToId.keys());
    print('[pubmed-citation-LDA]: venue number {0}'.format(venueNum));
    print('[pubmed-citation-LDA]: topic summary generation');
    topicSummary = getTopicSummary(pmd, pmidToId, idToPmid, ldaInstance, topDocCnt=10, topTokCnt=20);
    print('[pubmed-citation-LDA]: topic summary dump');
    dumpShortTopicSummary(topicSummary, ldaFilePath + '_shortsummary');
    return;

def pubmedCitationPaperSelfCitation(ldaFilePath):
    print('[pubmed-citation-paper-self-citation]: loading lda');
#    ldaFilePath = os.path.join(variables.RESULT_DIR, 'pubmed_citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_10_10.lda');
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath);
    print('[pubmed-citation-paper-self-citation]: loading pubmed');
    pmd = getPubMedCorpus();
    print('[pubmed-citation-paper-self-citation]: indexing');
    (pmidToId, idToPmid) = getCitMetaGraphPmidIdMapping(pmd);
    venueNum = pmd.getVenueNum(pmidToId.keys());
    print('[pubmed-citation-paper-self-citation]: venue number {0}'.format(venueNum));
    paperCitedCntDict = {};
    paperSelfCitationProbDict = {};
    totalCitedCnt = 0;
    print('[pubmed-citation-paper-self-citation]: counting cited number');
    for citingPmid in pmd.citMetaGraph:
        for citedPmid in pmd.citMetaGraph[citingPmid]:
            paperCitedCntDict[citedPmid] = paperCitedCntDict.get(citedPmid, 0.0) + pmd.citMetaGraph[citingPmid][citedPmid];
            totalCitedCnt += pmd.citMetaGraph[citingPmid][citedPmid];
    print('[pubmed-citation-paper-self-citation]: counting cited number data_size={0}'.format(totalCitedCnt));
    print('[pubmed-citation-paper-self-citation]: counting self citation prob');
    for pmid in pmidToId: paperSelfCitationProbDict[pmid] = sum([ldaInstance.phiEstimate[k][pmidToId[pmid]] * 
                                                                 ldaInstance.thetaEstimate[pmidToId[pmid]][k]  
                                                                 for k in range(ldaInstance.K)])
    (paperCitedCntDictRankToKey, paperCitedCntDictKeyToRank) = toolkit.utility.getDictRank(paperCitedCntDict, lambda x: paperCitedCntDict[x], reverse=True);
    (paperSelfCitationProbDictRankToKey, paperSelfCitationProbDictKeyToRank) = toolkit.utility.getDictRank(paperSelfCitationProbDict, lambda x: paperSelfCitationProbDict[x], reverse=True);
    dumpFilePath = ldaFilePath + '_selfCit_probSorted';
    dumpFile = open(dumpFilePath, 'w');
    for r in range(len(paperSelfCitationProbDict)):
        
        pmid = paperSelfCitationProbDictRankToKey[r];
        
        rCitedCnt = paperCitedCntDictKeyToRank.get(pmid, 0);
        citedCnt = paperCitedCntDict.get(pmid, -1);
        
        rSelfCited = paperSelfCitationProbDictKeyToRank[pmid];
        selfCitedProb = paperSelfCitationProbDict[pmid];
                
        title = pmd.docs[pmid]['title'];
        dumpFile.write('CitedCnt= {0:>6}({1:>6})\t SelfCitedProb= {2:.6f}({3:>6}): {4}\n'.format(citedCnt, rCitedCnt, selfCitedProb, rSelfCited, title));
    dumpFile.close();
    return;
    
def pubmedCitationMatrix(ldaFilePath):
    print('[pubmed-citation-LDA]: loading lda');
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath);
    citMatrix = getCitationMatrix(ldaInstance);
    citMatrixFile = open(ldaFilePath + '_citMatrix', 'w');
    citMatrixFile.write('\n'.join([' '.join([str(x) for x in vec]) for vec in citMatrix]));
    citMatrixFile.close();
    return;

def pubmedTimeSortedCitationMatrix(citMatrixFilePath, topicSummaryFilePath):
    print('[Time Sorted Citation Matrix]: read citation file: {0}'.format(citMatrixFilePath));
    citMatrix = readCitMatrixSummary(citMatrixFilePath);
    print('[Time Sorted Citation Matrix]: read topic summary file: {0}'.format(topicSummaryFilePath));
    topicSummaryDict = readTopicSummary(topicSummaryFilePath);
    print('[Time Sorted Citation Matrix]: sort topic on time');
    timeSortedTopicIdLst = [topicId for topicId in sorted(topicSummaryDict, key=lambda x: topicSummaryDict[x][2])];
    print('[Time Sorted Citation Matrix]: sort topic on time -- read {0} topics'.format(len(timeSortedTopicIdLst)));
    print('[Time Sorted Citation Matrix]: compute time sorted citation matrix');
    timeSortedCitMatrix = [[citMatrix[k1][k2] for k2 in timeSortedTopicIdLst] for k1 in timeSortedTopicIdLst];
    timeSortedCitMatrixFilePath = citMatrixFilePath + '_timeSorted';
    print('[Time Sorted Citation Matrix]: dump time sorted citation matrix file {0}'.format(timeSortedCitMatrixFilePath));
    timeSortedCitMatrixFile = open(timeSortedCitMatrixFilePath, 'w');
    timeSortedCitMatrixFile.write('\n'.join([' '.join([str(x) for x in vec]) for vec in timeSortedCitMatrix]));    
    return timeSortedCitMatrix;
    
def pubmedTimeSortedShortTopicSummary(topicSummaryFilePath):
    print('[Time Sorted Short Summary]: read summary file {0}'.format(topicSummaryFilePath));
    topicSummaryDict = readTopicSummary(topicSummaryFilePath);    
    dumpFile = open(topicSummaryFilePath + '_timeSorted_shortSummary', 'w');
    timeSort = 0;
    for k in sorted(topicSummaryDict, key=lambda k:topicSummaryDict[k][2]):
        sys.stdout.write('\r[Time Sorted Short Summary]: read topic {0}'.format(k));
        sys.stdout.flush();
        (topicId, topicProb, topicYearMean, topicYearVar, topDocs, topToks, topVens) = topicSummaryDict[k];
        dumpFile.write('[timeSort:{0},\tTopic: {1}]:\t{2:.6f}  year={3:.2f}({4:.2f})\t'.format(timeSort, k, topicProb, topicYearMean, topicYearVar));
        for topTok in topToks: dumpFile.write('{0} '.format(topTok[1]));
        dumpFile.write('\n');
        timeSort += 1;
    print('');
    dumpFile.close();
    
if(__name__ == '__main__'):
    #===========================================================================
    # RUN LDA
    #===========================================================================
#    pubmedCitationLdaRun();
    
    #===========================================================================
    # READ LDA FILE
    #===========================================================================
#    pubmedCitationLdaSummary();    
    
    #===========================================================================
    # RUN TIME SORTED CITATION MATRIX
    #===========================================================================
#    pubmedTimeSortedCitationMatrix('/home/xwang95/result/pubmed_citation_lda/pubmed_citation_lda_100_145317_145317_0.001_0.001_timeCtrl_30_45.lda_citMatrix',
#                                   '/home/xwang95/result/pubmed_citation_lda/pubmed_citation_lda_100_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary')
    #ldaFilePath1 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda', 'pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_10_10.lda');
    #ldaFilePath2 = os.path.join(toolkit.variables.RESULT_DIR, 'pubmed_citation_lda', 'pubmed_citation_lda_100_145317_145317_0.001_0.001_timeCtrl_30_45.lda');
    #pubmedCitationPaperSelfCitation(ldaFilePath2);
    ldaFilePath1 = 'C:/Users/rbrto/Documents/citation_lda/pubmed_citation_lda_500_145317_145317_0.001_0.001_timeCtrl_30_45.lda_summary';
    ts = readTopicSummary(ldaFilePath1)
    pass;
