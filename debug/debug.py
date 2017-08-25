'''
Created on Jan 29, 2013

@author: xwang95
'''
import deep_nlp.sentiment
import nltk
import toolkit.utility;
import re;
from toolkit import utility;
import time
import os.path;
from toolkit import variables

def func(a, b=None, c=None):
    return a - c;


if(__name__ == '__main__'):
    #===========================================================================
    # sentimentAnalyzer = deep_nlp.sentiment.SentimentAnalyzer('/home/xwang95/resource/lex/clues.lex');
    # raw = "Today is a good day. I love to eat. My name is Jacob Perkins";
    # sents = nltk.sent_tokenize(raw);
    # for sent in sents:
    #    words = nltk.word_tokenize(sent);
    #    postags = nltk.tag.pos_tag(words);
    #    print postags      
    # pass
    # 
    #===========================================================================
    
    #===========================================================================
    # file = open('test.txt');
    # print(toolkit.utility.readUntil(lambda line: (line == '</FILE>'), file));
    # print(toolkit.utility.readUntil(lambda line: (line == '</FILE>'), file));
    #===========================================================================
    
    #===========================================================================
    # tag = re.compile('ab(.*?),(.*?)ef')
    # a = 'ab123,456ef ab111,222ef';
    # for m in tag.finditer(a): 
    #    (x,y) = m.groups();
    #    print x,y
    #===========================================================================
    
    #===========================================================================
    # a = range(5)
    # for i in a:
    #    print i;
    #    i =  i*2;
    #===========================================================================
    
    #===========================================================================
    # while(True):
    #    utility.printProgressBar(time.clock()/10);
    #    if(time.clock()>=10): break;
    # print('');
    # print('abcde');
    #===========================================================================
    
    #===========================================================================
    # a = [1,2,3,4,5,6][0:4];
    # print a
    #===========================================================================
    
    #===========================================================================
    # d = {1:0.2,2:0.2,3:0.2,4:0.2,5:0.2};
    # print toolkit.utility.getDistExpectation(d);
    # print toolkit.utility.getDistVariation(d, 3);
    #===========================================================================
    
    pass;
