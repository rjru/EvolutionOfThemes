'''
Created on Nov 3, 2012

@author: xiaolong
'''

class SentimentAnalyzer(object):
    '''
    classdocs
    '''
    
    lex = {};
    posLexNum = 0;
    negLexNum = 0;
    neuLexNum = 0;
    
    def loadLexicon(self, lexFilePath):
        lexFile = open(lexFilePath, 'r');
        
        for line in lexFile:
            if(line.startswith('//')): continue;
            parts = line.strip().split();
            if(len(parts) != 6): continue;
            entry = {};
            entry['word'] = parts[0];
            if(parts[1] != '-'): entry['pos'] = parts[1];
            if(parts[2] != '-'): entry['stem'] = parts[2];
            if(parts[3] != '-'): entry['domain'] = parts[3];
            entry['polarity'] = self.parseNumVal(parts[4]);
            entry['confidence'] = self.parseNumVal(parts[5]);
            if(entry['polarity'] > 0): self.posLexNum += 1;
            elif(entry['polarity'] == 0): self.neuLexNum += 0;
            else: self.negLexNum += 1; 
            self.lex[entry['word']] = entry;
        lexFile.close();
        print("[Sentiment Analyzer]: Loading {0} Lexicons".format(len(self.lex)));
        print("[Sentiment Analyzer]: {0:>10} Positive Lexicons".format(self.posLexNum));
        print("[Sentiment Analyzer]: {0:>10} Negative Lexicons".format(self.negLexNum));
        print("[Sentiment Analyzer]: {0:>10} Neutral  Lexicons".format(self.neuLexNum));
        
    
    
    '''safely return parsed num value wihtout exception'''
    def parseNumVal(self, str):
        try:
            v = int(str);
        except:
            try:
                v = float(str);
            except:
                v = 0;
        return v;
    
    def __init__(self, lexFilePath):
        '''
        Constructor
        '''
        lex = {};
        posLexNum = 0;
        negLexNum = 0;
        neuLexNum = 0;
        self.loadLexicon(lexFilePath);
        pass;