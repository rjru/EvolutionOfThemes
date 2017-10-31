import theme_discovery.citation_based_method;

if __name__ == '__main__':



    burninHr = 3  #1.2 30
    sampliHr = 4.5  #1.8 45
    number_themes = 90  #[32, 256]

    theme_discovery.citation_based_method.pubmedCitationLdaRun(number_themes, burninHr, sampliHr);
    #result_name = "C:/Users/rbrto-pc/Documents/test_4/result/pubmed_citation_lda_"+str(number_themes)+"_11624_11624_0.001_0.001_timeCtrl_"+str(burninHr)+"_"+str(sampliHr)+".lda";
    #theme_discovery.citation_based_method.pubmedCitationLdaSummary(result_name)

 #   for num_t in number_themes:
 #       theme_discovery.citation_based_method.pubmedCitationLdaRun(num_t, burninHr, sampliHr);
 #       result_name = "C:/Users/rbrto-pc/Documents/test_3/result/pubmed_citation_lda_"+str(num_t)+"_11624_11624_0.001_0.001_timeCtrl_"+str(burninHr)+"_"+str(sampliHr)+".lda";
 #       theme_discovery.citation_based_method.pubmedCitationLdaSummary(result_name)  # holaa
