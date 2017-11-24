
from toolkit import utility, variables
import os.path;
from corpus.pubmed import PubMed
from deep_nlp.text import wordTokenize;
from theme_discovery.citation_based_method import readTopicSummary
from collections import Counter
from nltk import *
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

with open("C:/Users/rbrto-pc/Google Drive/citation_lda/src/clustering_process/vectorTotal.tfidf", 'rb') as pickle_file:
    print("LOAD")
    tfs = pickle.load(pickle_file)
    print("calculando matrix")
    m = open('vectorcosineTotal.csv', 'w')
    for a in tfs:
        for b in tfs:
            cs = cosine_similarity(a, b)
            w = str(abs((cs - 1).round(8))[0][0])+";"
            m.write(w)
        m.write("\n")
    print("finishhh")
