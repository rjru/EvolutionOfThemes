'''
Created on Nov 3, 2012

@author: xiaolong
'''
from sentiment import SentimentAnalyzer;
import nltk;
from toolkit import variables
import os;

if __name__ == '__main__':
    sentimentAnalyzer = SentimentAnalyzer(os.path.join(variables.RESOURCE_DIR, 'lex/clues.lex'));
    raw = "Today is a good day. I love to eat. My name is Jacob Perkins";
    sents = nltk.sent_tokenize(raw);
    for sent in sents:
        words = nltk.word_tokenize(sent);
        postags = nltk.tag.pos_tag(words);
        print (postags)      
    pass
