
from theme_discovery import citation_based_method
from theme_discovery import theme_evolution
from clustering_process.clustering import *

if __name__ == '__main__':

    burninHr = 1#3
    sampliHr = 1.5#4.5
    number_themes = [20, 40, 80, 100]

    #for num_t in number_themes:
        #citation_based_method.pubmedCitationLdaRun(num_t, burninHr, sampliHr);
        #pubmed_citation_lda_40_12954_12954_0.001_0.001_timeCtrl_1_1.5
    num_t = 20
    result_name = "C:/Users/rbrto-pc/Documents/tests/test_6/result/pubmed_citation_lda_" + str(num_t) + "_12954_12954_0.001_0.001_timeCtrl_" + str(burninHr) + "_" + str(sampliHr) + ".lda"
    #citation_based_method.pubmedCitationLdaSummary(result_name)
    result_name = result_name + "_summary"
    topicsSumary = readTopicSummary(result_name)
    #print(num_t)
    #theme_evolution.printVenEntropy(result_name)
    file_lda = "pubmed_citation_lda_" + str(num_t) + "_12954_12954_0.001_0.001_timeCtrl_" + str(burninHr) + "_" + str(sampliHr)
    generateJsonbyClustering(file_lda, 'pubCit_20_content_dtw.json')
