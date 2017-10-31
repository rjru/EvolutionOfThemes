import os
cpt = sum([len(files) for r, d, files in os.walk("F:/PUBMED/pubmed/articles.A-B.xml/3_Biotech")])

dir_root = 'F:/PUBMED/pubmed/'
dir_pubmed = ['articles.A-B.xml', 'articles.C-H.xml', 'articles.I-N.xml', 'articles.O-Z.xml']
res_file_pubmed = open("testfile.txt", "w")

for part_pubmed in dir_pubmed:
    print(dir_root+part_pubmed)
    for sub_dir in os.listdir(dir_root+part_pubmed):
        sub_dir_path = dir_root + part_pubmed + "/" + sub_dir
        cpt = sum([len(files) for r, d, files in os.walk(sub_dir_path)])
        #print(sub_dir_path, ", ", cpt)
        res_1 = sub_dir_path + ", " + str(cpt)+"\n"
        res_file_pubmed.write(res_1)