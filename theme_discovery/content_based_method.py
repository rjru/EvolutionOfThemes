'''
Created on Feb 14, 2013

@author: xwang95
'''
import corpus.pubmed;
import toolkit.utility;
import topic_modeling.lda;
import os.path;
import deep_nlp.text;
import sys;
from toolkit import variables;
import re;

def contentLdaRun(data, K, D, W, alpha, beta, burninTimeHr, sampliTimeHr, dumpFileFolder, contentField):
    dumpFilePath = os.path.join(dumpFileFolder, 'pubmed_content_{8}_lda_{0}_{1}_{2}_{3}_{4}_{5}_{6}_{7}.lda'.format(K, D, W, alpha, beta, 'timeCtrl', burninTimeHr, sampliTimeHr, contentField));
    toolkit.utility.removePath(dumpFilePath);
    ldaInstance = topic_modeling.lda.LDA(data, K, D, W, alpha, beta, burnTime=burninTimeHr, sampTime=sampliTimeHr, iterCtrl=False);
    (postTheta, postPhi, topicWeights) = ldaInstance.Mcmc();
    topic_modeling.lda.dumpLdaEstimateFile(ldaInstance, dumpFilePath)
    return (postTheta, postPhi, topicWeights);

def filterTokLst(tokLst): return [tok for tok in tokLst if (len(tok) > 1)];

def getTopicSummary(pmd, pmidToId, idToPmid, tokToId, idToTok, ldaInstance, contentField, topDocCnt=20, topTokCnt=20, topVenueCnt=20):
    thetaMatrix = ldaInstance.thetaEstimate;
    phiMatrix = ldaInstance.phiEstimate;
    topWeiVec = ldaInstance.topWeiEstimate;
    topicDocMatrix = [[0.0 for d in range(ldaInstance.D)] for k in range(ldaInstance.K)];
    topicSummary = {};
    for id in range(len(thetaMatrix)):
        wrdCnt = len((pmd.docs[idToPmid[id]][contentField]).split());
        for k in range(ldaInstance.K): topicDocMatrix[k][id] += wrdCnt * thetaMatrix[id][k];
    for k in range(ldaInstance.K): topicDocMatrix[k] = toolkit.utility.normalizeVector(topicDocMatrix[k]);        
    for k in range(ldaInstance.K):
        sys.stdout.write('\r[topic summary]: process topic {0}'.format(k));
        sys.stdout.flush();
        tokExptFreq = {};
        venueDist = {};
        yearDist = {};
        topDocs = [];
        topToks = [];
        for d in range(ldaInstance.D):
            prob = topicDocMatrix[k][d];
            pmid = idToPmid[d];
            venue = pmd.docs[pmid]['venue'];
            year = pmd.docs[pmid]['year'];
            venueDist[venue] = venueDist.get(venue, 0.0) + prob;
            yearDist[year] = yearDist.get(year, 0.0) + prob;
        topDocId = [d for d in sorted(range(ldaInstance.D), key=lambda x: topicDocMatrix[k][x], reverse=True)][0:topDocCnt];
        topDocs = [(topicDocMatrix[k][d], pmd.docs[idToPmid[d]]['venue'], pmd.docs[idToPmid[d]]['title']) for d in topDocId];
        topTokId = [t for t in sorted(range(ldaInstance.W), key=lambda x: phiMatrix[k][x], reverse=True)][0:topTokCnt];
        topToks = [(phiMatrix[k][id], idToTok[id]) for id in topTokId];
        
        topVenueId = [venue for venue in sorted(venueDist, key=lambda x:venueDist[x], reverse=True)][0:topVenueCnt];
        topVenues = [(venueDist[venue], venue) for venue in topVenueId];
        topicSummary[k] = (topToks, venueDist, yearDist, topWeiVec[k], topDocs, topVenues);
    print('');           
    return topicSummary;                 
    return;

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



NOT_FOLD = True;
#===============================================================================
# API
#===============================================================================
def pubmedContentLdaRun(topicNum, burninHr, sampliHr, threshold=10, contentField='abstract'):
    dumpFileFolder = os.path.join(variables.RESULT_DIR, 'pubmed_content_{0}_lda/'.format(contentField));
    '''data loading'''
    print('[pubmed-content-LDA]: loading pubmed');
    pmd = corpus.pubmed.getPubMedCorpus();
    print('[pubmed-content-LDA]: indexing (threshold={0},field={1})'.format(threshold, contentField));
    # conteo de palabras
    freqWrdCntDict = corpus.pubmed.getContentFreqWrdCntDict(pmd, contentField=contentField);
    (tokToId, idToTok) = corpus.pubmed.getContentTokIdMapping(pmd, freqWrdCntDict, threshold, contentField=contentField);
    (pmidToId, idToPmid) = corpus.pubmed.getContentPmidIdMapping(pmd);
    D = len(pmidToId);
    W = len(tokToId);
    print('                       D={0}, W={1}'.format(D, W));
    print('[pubmed-content-LDA]: insert tuple (doc, wrd, cnt) to list');
    data = corpus.pubmed.getContentDocWrdCntTupleLst(pmd, tokToId, idToTok, pmidToId, idToPmid, freqWrdCntDict, threshold, contentField);
    print('                       data size: {0}'.format(len(data)));
    '''running LDA'''
    (postTheta, postPhi, topicWeights) = contentLdaRun(data, topicNum, D, W, 1e-3, 1e-3, burninHr, sampliHr, dumpFileFolder, contentField);    
    return;

def pubmedContentLdaSummary(ldaFilePath, threshold=10, contentField='title'):
    print('[pubmed-content-LDA]: loading lda');
    ldaInstance = topic_modeling.lda.readLdaEstimateFile(ldaFilePath);
    print('[pubmed-content-LDA]: loading pubmed');
    pmd = corpus.pubmed.getPubMedCorpus();
    print('[pubmed-content-LDA]: indexing (threshold={0},field={1})'.format(threshold, contentField));
    freqWrdCntDict = corpus.pubmed.getContentFreqWrdCntDict(pmd, contentField=contentField);
    (tokToId, idToTok) = corpus.pubmed.getContentTokIdMapping(pmd, freqWrdCntDict, threshold, contentField=contentField);
    (pmidToId, idToPmid) = corpus.pubmed.getContentPmidIdMapping(pmd);
    venueNum = pmd.getVenueNum(pmidToId.keys());
    print('[pubmed-citation-LDA]: venue number {0}'.format(venueNum));
    print('[pubmed-citation-LDA]: topic summary generation');
    topicSummary = getTopicSummary(pmd, pmidToId, idToPmid, tokToId, idToTok, ldaInstance, contentField, topDocCnt=10, topTokCnt=20);
    print('[pubmed-citation-LDA]: topic summary dump');
    dumpTopicSummary(topicSummary, ldaFilePath + '_summary');
    dumpShortTopicSummary(topicSummary, ldaFilePath + '_shortsummary');
    return;

if(__name__ == '__main__'):
#    pubmedContentLdaRun(100, 0.2, 0.2, contentField='title');
    ldaFilePath = '/home/xwang95/result/pubmed_content_title_lda/pubmed_content_title_lda_500_317975_22312_0.001_0.001_timeCtrl_12_12.lda';
    ldaFilePath = '/home/xwang95/result/pubmed_content_title_lda/pubmed_content_title_lda_100_317975_22312_0.001_0.001_timeCtrl_12_12.lda';
    pubmedContentLdaSummary(ldaFilePath);
