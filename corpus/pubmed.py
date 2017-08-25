'''
Created on Nov 4, 2012

@author: xiaolong
'''
import toolkit.utility
import os
import os.path
import re
# import regex as re
import sys
from toolkit import utility, variables
import toolkit


class PubMed(object):
    # ===========================================================================
    # docs: DICT (pmid -> TABLE)
    #    'pmid': pmid,
    #    'title': title,
    #    'venue': venue,
    #    'year': year,
    #    'filePath': filePath
    #    'abstract': abstract
    #    'citLst': LST (TABLE)
    #        'citingDocPmid':citingDocPmid,
    #        'citedDocPmid':citedDocPmid,
    #        'coCitedDocPmidLst':coCitedDocPmidLst,
    #        'txt':txt
    # ===========================================================================
    docs = None
    numDocs = None
    metaDataFilePath = None
    citFilePath = None
    abstractFilePath = None
    # bodyFilePath = None
    # ===========================================================================
    # citMetaGraph: DICT (citingDocPmid -> DICT: (citedDocPmid -> cnt))
    # ===========================================================================
    citMetaGraph = None

    def __init__(self, metaDataFilePath=None, citFilePath=None, abstractFilePath=None, bodyFilePath=None):
        self.docs = {}
        self.metaDataFilePath = metaDataFilePath
        self.citFilePath = citFilePath
        self.abstractFilePath = abstractFilePath
        self.bodyFilePath = bodyFilePath
        if (self.metaDataFilePath is not None): self.readMetaDataFile()
        if (self.citFilePath is not None): self.readCitationFile()
        if (self.abstractFilePath is not None): self.readAbstractFile()
        if (self.bodyFilePath is not None): self.readBodyFile()

    def readMetaDataFile(self):
        metaDict = readMetaFile(self.metaDataFilePath)
        cnt = 0
        for pmid in metaDict:
            if (pmid not in self.docs): self.docs[pmid] = {}
            self.docs[pmid].update(metaDict[pmid])
            cnt += 1

        self.numDocs = len(self.docs)
        print('[PubMed] MetaData {0} entries (#pmid)'.format(cnt))
        return

    def readCitationFile(self):
        (citMetaGraph, citDict) = readCitationFile(self.citFilePath)
        self.citMetaGraph = citMetaGraph
        cnt = 0
        for pmid in citDict:
            if pmid in self.docs:
                self.docs[pmid]['citLst'] = citDict[pmid]
                cnt += 1
        print('[PubMed] citations {0} entries (#citing paper)'.format(cnt))
        print('[PubMed] citing docs {0} (#edges)'.format(len(self.citMetaGraph)))
        # =======================================================================
        # reportCitMetaGraph(self.citMetaGraph)
        # =======================================================================
        return

    def readAbstractFile(self):
        pmidAbsTupleLst = readAbstractFile(self.abstractFilePath)
        for (pmid, abs) in pmidAbsTupleLst: self.docs[pmid]['abstract'] = abs
        print('[PubMed] abstracts {0} (#abstract)'.format(len(pmidAbsTupleLst)))
        return

    def readBodyFile(self):
        pmidBodyTupleLst = readBodyFile(self.bodyFilePath)
        for (pmid, abs) in pmidBodyTupleLst: self.docs[pmid]['body'] = abs
        print('[PubMed] bodys {0} (#body)'.format(len(pmidBodyTupleLst)))
        return

    def getVenueNum(self, pmidSet=None):
        venueSet = set()
        if (pmidSet is None):
            for doc in self.docs: venueSet.add(self.docs[doc]['venue'])
        else:
            for doc in pmidSet:
                venueSet.add(self.docs[doc]['venue'])
        return len(venueSet)


NOT_FOLD = True


# ===============================================================================
# metaDict[pmid] = {'pmid': pmid, 'title': title, 'venue': venue, 'year': year, 'filePath': filePath}
# ===============================================================================
def readMetaFile(metaFilePath):
    metaFile = open(metaFilePath, 'r')
    metaDict = {}
    eof = False
    while (not eof):  # no es la mejor manera porque a veces le un bloque extra
        (lines, eof) = toolkit.utility.readLines(6, metaFile)
        if (eof == True): break  # fix for roberto
        pmid = toolkit.utility.parseNumVal(toolkit.utility.rmLeadingStr(lines[0], 'pmid = '))
        title = toolkit.utility.rmLeadingStr(lines[1], 'title = ')
        venue = toolkit.utility.rmLeadingStr(lines[2], 'venue = ')
        year = toolkit.utility.parseNumVal(toolkit.utility.rmLeadingStr(lines[3], 'year = '))
        filePath = toolkit.utility.rmLeadingStr(lines[4], 'path = ')
        metaDict[pmid] = {'pmid': pmid, 'title': title, 'venue': venue, 'year': year, 'filePath': filePath,
                          'abstract': ""}
    metaFile.close()
    return metaDict


NOT_FOLD = True


# ===============================================================================
# (citMetaGraph, citDict)
# citDict[citingDocPmid].append({'citingDocPmid':citingDocPmid, 'citedDocPmid':citedDocPmid, 'coCitedDocPmidLst':coCitedDocPmidLst, 'txt':txt})
# ===============================================================================
def readCitationFile(citationFilePath):
    citFile = open(citationFilePath, 'r')  # open instaned file
    citDict = {}
    citMetaGraph = {}
    eof = False
    while (not eof):
        (lines, eof) = toolkit.utility.readLines(5, citFile)
        if eof == True: continue  # fix bug rjru
        citingDocPmid = toolkit.utility.parseNumVal(lines[0])
        citedDocPmid = toolkit.utility.parseNumVal(lines[1])
        coCitedDocPmidLst = [toolkit.utility.parseNumVal(part) for part in lines[2].strip('[]').split(',')]
        txt = lines[3]
        if (citingDocPmid not in citDict): citDict[citingDocPmid] = []
        citDict[citingDocPmid].append(
            {'citingDocPmid': citingDocPmid, 'citedDocPmid': citedDocPmid, 'coCitedDocPmidLst': coCitedDocPmidLst,
             'txt': txt})
        if (citingDocPmid not in citMetaGraph): citMetaGraph[citingDocPmid] = {}
        if (citedDocPmid not in citMetaGraph[citingDocPmid]): citMetaGraph[citingDocPmid][citedDocPmid] = 0
        citMetaGraph[citingDocPmid][citedDocPmid] += 1
    return (citMetaGraph, citDict)


NOT_FOLD = True


# ===============================================================================
# pmidAbsTupleLst: list of (pmid, abs)
# ===============================================================================
def readAbstractFile(abstractFilePath):
    abstractFile = open(abstractFilePath, 'r')  # open instead file
    pmidAbsTupleLst = []
    eof = False
    while (not eof):
        (lines, eof) = toolkit.utility.readLines(2, abstractFile)  # esto dara un error porque a pesar de ser el final del archivo, seguira leyendo

        if (eof == True): break  # fix for roberto

        pmid = toolkit.utility.parseNumVal(lines[0])
        abs = lines[1]
        pmidAbsTupleLst.append((pmid, abs))
    abstractFile.close()
    return pmidAbsTupleLst


def readBodyFile(bodyFilePath):
    bodyFile = open(bodyFilePath, 'r')  # open instead file
    pmidBodyTupleLst = []
    eof = False
    while (not eof):
        (lines, eof) = toolkit.utility.readLines(2, bodyFile)

        if (eof == True): break  # fix for roberto

        pmid = toolkit.utility.parseNumVal(lines[0])
        abs = lines[1]
        pmidBodyTupleLst.append((pmid, abs))
    bodyFile.close()
    return pmidBodyTupleLst


NOT_FOLD = True
# ===============================================================================
# pubmed Utility
# ===============================================================================
titleTag = re.compile(r'<article-title.*?>(.*?)</article-title>', re.MULTILINE | re.DOTALL)
whiteSpaceTag = re.compile('\s+', re.MULTILINE | re.DOTALL)
htmlTag = re.compile('<.{,100}?>', re.MULTILINE | re.DOTALL)
fontTag = re.compile('&#x.*? ', re.MULTILINE | re.DOTALL)
docRefLstTag = re.compile(r"""<FILE>\n<NAME>(.*?)</NAME>\n(.*?)</FILE>""", re.DOTALL)
refTag = re.compile(
    '<ref id="(.*?)">.*?<article-title.*?>(.*?)</article-title>.*?<pub-id pub-id-type="pmid">(.*?)</pub-id>', re.DOTALL)
contextTag = re.compile('<REFCONTEXT>\n(.*?)</REFCONTEXT>', re.DOTALL)
refContextTag = re.compile(r"""\[?<xref ref-type="bibr" rid="(.*?)">(.*?</xref>\]?)?""", re.DOTALL)
htmlBrokenTag = re.compile(r"</\w{,100}?>?|<?/\w{,100}>", re.DOTALL)
pmidTag = re.compile('<article-id pub-id-type="pmid">(.*?)</article-id>')
refPmidTag = re.compile('--ref_pmid=(.*?)--')
# abstractTag = re.compile(r'<abstract>(.*?)</abstract>', re.DOTALL)
abstractTag = re.compile(r'<abstract>(.*?)</abstract>', re.DOTALL)
bodyTag = re.compile(r'<body>(.*?)</body>', re.DOTALL)
dateTag = re.compile(r'<date date-type=\"received\">(.*?)<year>(.*?)</year></date>')  # esto yo hice :')
refTag2 = re.compile('<ref id="(.*?)">(.*?)</ref>', re.DOTALL)


def reportCitMetaGraph(citMetaGraph):
    citingDocHist = {}
    citingCntHist = {}
    for citingDocId in citMetaGraph:
        citingDoc = len(citMetaGraph[citingDocId])
        citingCnt = sum(citMetaGraph[citingDocId].values())
        if (citingDoc not in citingDocHist): citingDocHist[citingDoc] = 0
        if (citingCnt not in citingCntHist): citingCntHist[citingCnt] = 0
        citingDocHist[citingDoc] += 1
        citingCntHist[citingCnt] += 1
    m = max(max(citingDocHist.keys()), max(citingCntHist.keys()))
    print('[PubMed Citing Meta Graph]: report:')
    print('                          : {0:<20}{1:<20}{2:<20}'.format('i', 'citingDocHist[i]', 'citingCntHist[i]'))
    for i in range(m):
        if ((i in citingDocHist) or (i in citingCntHist)):
            print('                          : {0:<20}{1:<20}{2:<20}'.format(i, citingDocHist.get(i, 0),
                                                                             citingCntHist.get(i, 0)))
    return


def generateMetaFile(pubmedFolderPathLst, metaFilePath):
    toolkit.utility.removePath(metaFilePath)

    metaFile = open(metaFilePath, 'w', encoding='utf8')  # encoding añadido
    cnt = 0
    jcnt = 0
    exceptCnt = 0
    for pubmedFolderPath in pubmedFolderPathLst:
        for journal in os.listdir(pubmedFolderPath):
            journalPath = os.path.join(pubmedFolderPath, journal)
            jcnt += 1

            #            print('[pubmed-metadata] processing venue: {0}'.format(journal))
            for doc in os.listdir(journalPath):
                filePath = os.path.join(journalPath, doc)
                file = open(filePath, 'r', encoding='utf8')  # encoding añadido
                txt = '\n'.join(file.readlines())
                # ===============================================================
                # DEBUG
                # ===============================================================
                if (not titleTag.search(txt)):
                    print("{0}: [{2}] {1}".format(exceptCnt, filePath, "no-title"))
                    exceptCnt += 1
                    continue
                    # ===============================================================
                # DEBUG end
                # ===============================================================
                title = titleTag.search(txt).group(1)
                title = cleanTitle(title)
                # ===============================================================
                # DEBUG
                # ===============================================================
                if (not pmidTag.search(txt)):
                    print("{0}: [{2}] {1}".format(exceptCnt, filePath, "no--pmid"))
                    exceptCnt += 1
                    continue
                # ===============================================================
                # DEBUG end
                # ===============================================================
                pmid = toolkit.utility.parseNumVal(pmidTag.search(txt).group(1))
                if (not dateTag.search(txt)):
                    year = "no year"
                    # aqui colocaremos para los que no tengan año no se almacenen
                    continue
                else:
                    year = dateTag.search(txt).group(2)
                file.close()
                # year = toolkit.utility.parseYear(filePath)[0]

                metaFile.write('pmid = {0}\n'.format(pmid))
                metaFile.write('title = {0}\n'.format(title))
                metaFile.write('venue = {0}\n'.format(journal))
                metaFile.write('year = {0}\n'.format(year))
                metaFile.write('path = {0}\n'.format(filePath))
                metaFile.write('\n')  # aqui hay un bug porque el final del archivo sobra un \n
                cnt += 1
    metaFile.close()
    print('[pubmed-metadata] processing {0} venues'.format(jcnt))
    print('[pubmed-metadata] processing {0} docs'.format(cnt))
    print('[pubmed-metadata] Exception Doc: {0}'.format(exceptCnt))
    return


def generateCitFile(metaDict, citContextTxtFilePathLst, citFilePath):
    toolkit.utility.removePath(citFilePath)
    cnt = 0
    exceptCnt = 0
    misMatchCnt = 0
    entryCnt = 0
    pathToPmidDict = {}
    citFile = open(citFilePath, 'w')
    print('[pubmed-gen_cit_file]: mapping path to pmid')
    # guarda los ids con sus rutas donde debe estar el doc
    # C:/Users/rbrto/Documents/citation_lda/data/PubMed/pubmed\\Acta_Crystallogr_C\\PMC2631130.nxml': 18391373
    for pmid in metaDict: pathToPmidDict[metaDict[pmid]['filePath']] = pmid
    for citContextTxtFilePath in citContextTxtFilePathLst:
        print('[pubmed-gen_cit_file]: process context file: {0}'.format(citContextTxtFilePath))
        citContextTxtFile = open(citContextTxtFilePath)
        eof = False
        while (not eof):
            (chunkLst, eof) = toolkit.utility.readUntil(lambda line: (line == '</FILE>'), citContextTxtFile)
            chunk = '\n'.join(chunkLst)
            # docRefLstTag = re.compile(r"""<FILE>\n<NAME>(.*?)</NAME>\n(.*?)</FILE>""", re.DOTALL)
            chunkMatch = docRefLstTag.match(chunk)
            # ===================================================================
            # DEBUG
            # ===================================================================
            if (not chunkMatch):
                misMatchCnt += 1
                continue
            # ===================================================================
            # DEBUG end
            # ===================================================================
            (citingDocFilePath, chunk1) = chunkMatch.groups()
            citingDocFilePath = citingDocFilePath.strip().replace(
                '/mounts/timan1/disks/0/shared/Parikshit/FUSE/pubmed_data/',
                os.path.join(variables.DATA_DIR, 'PubMed/'))
            # ===================================================================
            # DEBUG
            # ===================================================================
            if (citingDocFilePath not in pathToPmidDict):
                #                print('{0}: [citing doc no pmid] {1}'.format(exceptCnt, citingDocFilePath))
                exceptCnt += 1
                continue
            # ===================================================================
            # DEBUG end
            # ===================================================================
            # hace de esta form para tener el Pmid
            citingDocFilePmid = pathToPmidDict[citingDocFilePath]
            # ===================================================================
            # DEBUG
            # ===================================================================
            sys.stdout.write(
                '\r    processing [{0:^10}] docs: pmid={1:<15} no_pmid_cnt={2:<15} entry_cnt={3:<20} mis_match_cnt={4:<15}'.format(
                    cnt, citingDocFilePmid, exceptCnt, entryCnt, misMatchCnt))
            sys.stdout.flush()
            cnt += 1
            # ===================================================================
            # DEBUG end
            # ===================================================================
            refIdToPmidDict = {}
            citDataLst = []
            # chunk1 es el contenido menos sin el <name>
            parts = [part.strip() for part in chunk1.split('</ref>') if (part.strip())]
            for part in parts:
                lines = part.split('\n')
                metaLine = lines[0]
                chunk2 = '\n'.join(lines[1:])  # aqui debe ir el <REFCONTEXT>
                # refTag = re.compile('<ref id="(.*?)">.*?<article-title.*?>(.*?)</article-title>.*?<pub-id pub-id-type="pmid">(.*?)</pub-id>', re.DOTALL)
                m = refTag.search(metaLine)
                if (not m): continue
                (refIdGroup, citedDocTitleGroup, citedDocPmidGroup) = m.groups()

                refId = refIdGroup.strip()
                citedDocTitle = cleanTitle(citedDocTitleGroup)
                citedDocPmid = toolkit.utility.parseNumVal(citedDocPmidGroup)
                # contextTag = re.compile('<REFCONTEXT>\n(.*?)</REFCONTEXT>', re.DOTALL)
                contextLst = [context.strip() for context in contextTag.findall(chunk2)]
                # ===============================================================
                # DEBUG
                # ===============================================================
                if (citedDocPmid not in metaDict): continue
                # ===============================================================
                # DEBUG end
                # ===============================================================
                citDataLst.append((refId, citedDocTitle, citedDocPmid, contextLst))
                refIdToPmidDict[refId] = citedDocPmid
            for (refId, citedDocTitle, citedDocPmid, contextLst) in citDataLst:
                for context in contextLst:
                    # refContextTag = re.compile(r"""\[?<xref ref-type="bibr" rid="(.*?)">(.*?</xref>\]?)?""", re.DOTALL)
                    # el -1 en el get es para que retorne ese valor en el caso que no encuentre nada
                    context = refContextTag.sub(
                        lambda x: ' --ref_pmid={0}-- '.format(refIdToPmidDict.get(x.group(1), -1)), context)
                    context = whiteSpaceTag.sub(' ', context)
                    context = htmlTag.sub(' ', context)
                    context = fontTag.sub(' ', context)
                    context = htmlBrokenTag.sub(' ', context)
                    context = context.lower()
                    context = ' '.join(context.split())
                    # refPmidTag = re.compile('--ref_pmid=(.*?)--')
                    coCitedDocPmidLst = [toolkit.utility.parseNumVal(pmidStr) for pmidStr in refPmidTag.findall(context)
                                         if (pmidStr != '-1')]
                    citFile.write('{0}\n'.format(citingDocFilePmid))
                    citFile.write('{0}\n'.format(citedDocPmid))
                    citFile.write('{0}\n'.format(coCitedDocPmidLst))
                    citFile.write('{0}\n'.format(context))
                    citFile.write('\n')
                    entryCnt += 1
                    #                    citFile.write('{0}\n'.format(citedDocTitle))
                    #                    citFile.write('{0}\n'.format(refId))
                    #                    citFile.write('{0}\n'.format(citingDocFilePath))
        citContextTxtFile.close()
        print('')
    citFile.close()
    return


def cleanTitle(title):
    t = title
    t = whiteSpaceTag.sub(' ', t)
    t = htmlTag.sub(' ', t)
    t = fontTag.sub('', t)
    t = t.lower()
    t = ' '.join(t.split())
    return t


def generateAbstractDataset(pubmedFolderPathLst):
    for i in range(len(pubmedFolderPathLst)):
        pubmedFolderPath = pubmedFolderPathLst[i]
        pubmedAbstractFolderPath = pubmedFolderPath.replace('PubMed', 'abstract')#'PubMed/abstract')
        for journal in os.listdir(pubmedFolderPath):
            journalPath = os.path.join(pubmedFolderPath, journal)
            journalAbsPath = os.path.join(pubmedAbstractFolderPath, journal)
            toolkit.utility.mkDir(journalAbsPath)
            for doc in os.listdir(journalPath):
                docPath = os.path.join(journalPath, doc)
                absPath = os.path.join(journalAbsPath, doc)
                docFile = open(docPath, 'r')
                txt = '\n'.join(docFile.readlines())
                absMatch = abstractTag.search(txt)
                if (absMatch):
                    absTxt = absMatch.group(1)
                    absTxt = whiteSpaceTag.sub(' ', absTxt)
                    absTxt = absTxt.replace('<title>Abstract</title>', ' ')
                    absTxt = htmlTag.sub(' ', absTxt)
                    absTxt = fontTag.sub(' ', absTxt)
                    absTxt = htmlBrokenTag.sub(' ', absTxt)
                    absTxt = absTxt.lower()
                    absTxt = ' '.join(absTxt.split())
                    absFile = open(absPath, 'w')
                    absFile.write(absTxt)
                    absFile.close()
                docFile.close()
    return


def generateAbstractFile(metaDataFilePath, citFilePath, absFilePath):
    # pmd = PubMed(metaDataFilePath, citFilePath, None)
    pmd = PubMed(metaDataFilePath, None, None)
    cnt = 0
    absFile = open(absFilePath, 'w')
    for pmid in pmd.docs:
        filePath = pmd.docs[pmid]['filePath']
        abstractFilePath = filePath.replace('PubMed', 'abstract')#'PubMed/abstract')
        if (not os.path.exists(abstractFilePath)): continue
        abstractFile = open(abstractFilePath, 'r')
        abstractTxt = ' '.join(('\n'.join(abstractFile.readlines())).split())
        absFile.write('{0}\n'.format(pmid))
        absFile.write('{0}\n'.format(abstractTxt))
        sys.stdout.write('\r' + toolkit.utility.rFillSpaces(
            '[pubmed abstract]: process [{0}] => [{1}]'.format(cnt, abstractFilePath)))
        sys.stdout.flush()
        cnt += 1
    print('')
    print('[PubMed] abstract {0} entries'.format(cnt))
    absFile.close()
    return


def generateBodyFile(metaDataFilePath, citFilePath, bodyFilePath):
    # pmd = PubMed(metaDataFilePath, citFilePath, None)
    pmd = PubMed(metaDataFilePath, None, None)
    cnt = 0
    bdyFile = open(bodyFilePath, 'w')
    for pmid in pmd.docs:
        filePath = pmd.docs[pmid]['filePath']
        bodyFilePath = filePath.replace('PubMed', 'PubMed/body')
        if (not os.path.exists(bodyFilePath)): continue
        bodyFile = open(bodyFilePath, 'r')
        bodyTxt = ' '.join(('\n'.join(bodyFile.readlines())).split())
        bdyFile.write('{0}\n'.format(pmid))
        bdyFile.write('{0}\n'.format(bodyTxt))
        sys.stdout.write(
            '\r' + toolkit.utility.rFillSpaces('[pubmed body]: process [{0}] => [{1}]'.format(cnt, bodyFilePath)))
        sys.stdout.flush()
        cnt += 1
    print('')
    print('[PubMed] body {0} entries'.format(cnt))
    bdyFile.close()
    return


def generateBodyDataset(pubmedFolderPathLst):  # extrae las pates importantes como son el title, abstract y body
    for i in range(len(pubmedFolderPathLst)):
        pubmedFolderPath = pubmedFolderPathLst[i]
        pubmedAbstractFolderPath = pubmedFolderPath.replace('PubMed', 'PubMed/body')
        for journal in os.listdir(pubmedFolderPath):
            journalPath = os.path.join(pubmedFolderPath, journal)
            journalAbsPath = os.path.join(pubmedAbstractFolderPath, journal)
            toolkit.utility.mkDir(journalAbsPath)
            for doc in os.listdir(journalPath):
                docPath = os.path.join(journalPath, doc)
                bodyPath = os.path.join(journalAbsPath, doc)
                docFile = open(docPath, 'r')
                txt = '\n'.join(docFile.readlines())
                bodyMatch = bodyTag.search(txt)

                if (bodyMatch):
                    bodyTxt = bodyMatch.group(1)
                    bodyTxt = whiteSpaceTag.sub(' ', bodyTxt)
                    bodyTxt = bodyTxt.replace('<title>Body</title>', ' ')
                    bodyTxt = htmlTag.sub(' ', bodyTxt)
                    bodyTxt = fontTag.sub(' ', bodyTxt)
                    bodyTxt = htmlBrokenTag.sub(' ', bodyTxt)
                    bodyTxt = bodyTxt.lower()
                    bodyTxt = ' '.join(bodyTxt.split())
                    corpusFile = open(bodyPath, 'w')
                    corpusFile.write(bodyTxt)
                    corpusFile.close()

                docFile.close()
    return


NOT_FOLD = True


# ===============================================================================
# API
# ===============================================================================
#def getPubMedCorpus(metaDataFilePath=os.path.join(variables.DATA_DIR, 'PubMed/pubmed_metadata.txt'),
#                    citFilePath=os.path.join(variables.DATA_DIR, 'PubMed/pubmed_citation.txt'),
#                    absFilePath=os.path.join(variables.DATA_DIR, 'PubMed/pubmed_abstract.txt')):
#    return PubMed(metaDataFilePath, citFilePath, absFilePath)

def getPubMedCorpus(metaDataFilePath=os.path.join(variables.TEST_RESOURCE, 'pubmed_metadata.txt'),
                    citFilePath=os.path.join(variables.TEST_RESOURCE, 'pubmed_citation.txt'),
                    absFilePath=os.path.join(variables.TEST_RESOURCE, 'pubmed_abstract.txt')):
    return PubMed(metaDataFilePath, citFilePath, absFilePath)

NOT_FOLD = True


# ===============================================================================
# Citation-based
# ===============================================================================
def getCitMetaGraphPmidIdMapping(pmd):
    pmidToId = {}
    idToPmid = {}
    id = 0
    for citingDocPmid in pmd.citMetaGraph:
        if (citingDocPmid not in pmidToId):
            pmidToId[citingDocPmid] = id
            idToPmid[id] = citingDocPmid
            id += 1
        for citedDocPmid in pmd.citMetaGraph[citingDocPmid]:
            if (citedDocPmid not in pmidToId):
                pmidToId[citedDocPmid] = id
                idToPmid[id] = citedDocPmid
                id += 1
    return (pmidToId, idToPmid)


# aqui en data se extrae una lista pero necesito los ids asi que a modificar
def getCitMetaGraphDocWrdCntTupleLst(pmd, pmidToId, idToPmid):
    data = []
    for citingDocPmid in pmd.citMetaGraph:
        for citedDocPmid in pmd.citMetaGraph[citingDocPmid]:
            data.append(
                (pmidToId[citingDocPmid], pmidToId[citedDocPmid], pmd.citMetaGraph[citingDocPmid][citedDocPmid]))
    return data


NOT_FOLD = True


# ===============================================================================
# Content-based
# ===============================================================================
def getContentFreqWrdCntDict(pmd, contentField='abstract'):
    freqWrdCntDict = {}
    for pmid in pmd.docs:
        toks = (pmd.docs[pmid][contentField]).split()
        for tok in toks: freqWrdCntDict[tok] = freqWrdCntDict.get(tok, 0) + 1
    return freqWrdCntDict


def getContentTokIdMapping(pmd, freqWrdCntDict=None, threshold=None, contentField='abstract'):
    tokToId = {}
    idToTok = {}
    for pmid in pmd.docs:
        toks = (pmd.docs[pmid][contentField]).split()
        for tok in toks:
            if (tok not in tokToId):
                if ((freqWrdCntDict is not None) and (freqWrdCntDict[tok] < threshold)): continue
                id = len(tokToId)
                tokToId[tok] = id
                idToTok[id] = tok
    return (tokToId, idToTok)


def getContentPmidIdMapping(pmd):
    pmidToId = {}
    idToPmid = {}
    for pmid in pmd.docs:
        if (pmid not in pmidToId):
            id = len(pmidToId)
            pmidToId[pmid] = id
            idToPmid[id] = pmid
    return (pmidToId, idToPmid)


def getContentDocWrdCntTupleLst(pmd, tokToId, idToTok, pmidToId, idToPmid, freqWrdCntDict=None, threshold=None,
                                contentField='abstract'):
    data = []
    for pmid in pmd.docs:
        doc = pmidToId[pmid]
        wrdCntDict = {}
        for tok in (pmd.docs[pmid][contentField]).split():
            if ((freqWrdCntDict is not None) and (freqWrdCntDict[tok] < threshold)): continue
            wrdCntDict[tokToId[tok]] = wrdCntDict.get(tokToId[tok], 0) + 1
        for wrd in wrdCntDict: data.append((doc, wrd, wrdCntDict[wrd]))
    return data


NOT_FOLD = True

refListTag = re.compile(r'<ref-list>(.*?)</ref-list>', re.DOTALL)
contextCut = re.compile(r'<xref ref-type="bibr" rid=(.*?)</xref>', re.DOTALL)
refTag = re.compile(
    '<ref id="(.*?)">.*?<article-title.*?>(.*?)</article-title>.*?<pub-id pub-id-type="pmid">(.*?)</pub-id>', re.DOTALL)


def generateCitContextFile(metaFilePath, citContextFilePath):
    metaFile = open(metaFilePath, 'r')
    metaDict = {}
    eof = False
    citContextFile = open(citContextFilePath, 'w')
    while (not eof):  # no es la mejor manera porque a veces le un bloque extra
        (lines, eof) = toolkit.utility.readLines(6, metaFile)
        if (eof == True): break  # fix for roberto
        pmid = toolkit.utility.parseNumVal(toolkit.utility.rmLeadingStr(lines[0], 'pmid = '))
        title = toolkit.utility.rmLeadingStr(lines[1], 'title = ')
        venue = toolkit.utility.rmLeadingStr(lines[2], 'venue = ')
        year = toolkit.utility.parseNumVal(toolkit.utility.rmLeadingStr(lines[3], 'year = '))
        filePath = toolkit.utility.rmLeadingStr(lines[4], 'path = ')
        metaDict[pmid] = {'pmid': pmid, 'title': title, 'venue': venue, 'year': year, 'filePath': filePath,
                          'abstract': ""}
        print('procesing doc:', pmid)
        docFile = open(filePath, 'r', encoding='utf8')
        docFileTxt = '\n'.join(docFile.readlines())
        citContextFile.write('<FILE>\n')
        citContextFile.write('<NAME>' + filePath + '</NAME>\n\n')
        # refMatch = refListTag.search(docFileTxt).group(1)
        # citContextFile.write(refMatch)
        # refTag2 = re.compile('<ref id="(.*?)">(.*?)</pub-id>', re.DOTALL)
        if re.findall(refTag2, docFileTxt):
            refListMarch = re.findall(refTag2, docFileTxt)
        else:
            print("no match in: ", pmid)
            continue

        for ref in refListMarch:
            citContextFile.write("<ref id=\"" + ref[0] + "\">" + ref[1] + "</pub-id>")
            citContextFile.write("\n")
            # print("<ref id=\""+ref[0]+"\">.*?<article-title.*?>"+ref[1]+"</article-title>.*?<pub-id pub-id-type="+"pmid"+">"+ref[2]+"</pub-id>")
            rexg = "\[?<xref ref-type=\"bibr\" rid=\"" + ref[0] + "\">(.*?</xref>\]?)?"
            # print(rexg)
            refContextTag = re.compile(rexg, re.DOTALL)
            refContextTxt = re.findall(refContextTag, docFileTxt)
            for refContext in refContextTxt:
                citContextFile.write('<REFCONTEXT>\n')
                citContextFile.write('<xref ref-type="bibr" rid="' + ref[0] + '">' + '</xref>')  # refContext[0]+']')
                citContextFile.write('</REFCONTEXT>\n')
            citContextFile.write("</ref>\n\n")
        citContextFile.write('</FILE>\n')
    metaFile.close()
    return metaDict


# ===============================================================================
# TEST
# ===============================================================================
if (__name__ == '__main__'):
    #    pubmedFolderPathA_B = os.path.join(variables.DATA_DIR, 'PubMed/pubmedA_B')
    #    pubmedFolderPathC_H = os.path.join(variables.DATA_DIR, 'PubMed/pubmedC-H')
    #    pubmedFolderPathI_N = os.path.join(variables.DATA_DIR, 'PubMed/pubmedI-N')
    #    pubmedFolderPathO_Z = os.path.join(variables.DATA_DIR, 'PubMed/pubmedO-Z')


    #    pubmedCitContextFilePathA_B = os.path.join(variables.DATA_DIR, 'PubMed/ContextOutputA-B.txt')
    #    pubmedCitContextFilePathC_H = os.path.join(variables.DATA_DIR, 'PubMed/ContextOutputC-H.txt')
    #    pubmedCitContextFilePathI_N = os.path.join(variables.DATA_DIR, 'PubMed/ContextOutputI-N.txt')
    #    pubmedCitContextFilePathO_Z = os.path.join(variables.DATA_DIR, 'PubMed/ContextOutputO-Z.txt')

    #    pubmedFolderPathLst = [pubmedFolderPathA_B, pubmedFolderPathC_H, pubmedFolderPathI_N, pubmedFolderPathO_Z]

    #    pubmedCitContextFilePathLst = [pubmedCitContextFilePathA_B, pubmedCitContextFilePathC_H, pubmedCitContextFilePathI_N, pubmedCitContextFilePathO_Z]


    # el numero de test se indicara en toolkit.variables test number
    pubmedFolderPathTest = os.path.join(variables.TEST_DATA, 'PubMed')
    pubmedCitContextFilePathTest = os.path.join(variables.TEST_RESOURCE, 'citContextFile.txt')
    pubmedFolderPathLst = [pubmedFolderPathTest]
    pubmedCitContextFilePathLst = [pubmedCitContextFilePathTest]

    metaDataFilePath = os.path.join(variables.TEST_RESOURCE, 'pubmed_metadata.txt')
    citFilePath = os.path.join(variables.TEST_RESOURCE, 'pubmed_citation.txt')
    absFilePath = os.path.join(variables.TEST_RESOURCE, 'pubmed_abstract.txt')
    bodyFilePath = os.path.join(variables.TEST_RESOURCE, 'pubmed_body.txt')
    # ===========================================================================
    # Genearte the MetaDataFile
    # ===========================================================================
    generateMetaFile(pubmedFolderPathLst, metaDataFilePath)
    # abc = readMetaFile(metaDataFilePath)
    # ===========================================================================
    # Generate Citation File
    # ===========================================================================
    #print("1. generate citation CONTEXT file")
    #generateCitContextFile(metaDataFilePath, pubmedCitContextFilePathTest)
    #print("2. generate citation file")
    #generateCitFile(readMetaFile(metaDataFilePath), pubmedCitContextFilePathLst, citFilePath)

    #print("3. generate abstract dataset")
    #generateAbstractDataset(pubmedFolderPathLst)
    #print("4. generate abstract file")
    #generateAbstractFile(metaDataFilePath, citFilePath, absFilePath)

    # ===========================================================================
    # Generate body File
    # ===========================================================================
    #generateBodyDataset(pubmedFolderPathLst)
    #generateBodyFile(metaDataFilePath, citFilePath, bodyFilePath)

    # ===========================================================================
    # PubMed Corpus
    # ===========================================================================
    # pubmed = PubMed(metaDataFilePath, citFilePath, absFilePath)
    # ===========================================================================
    # API Example
    # ===========================================================================
    # pmd = getPubMedCorpus()
    pass
