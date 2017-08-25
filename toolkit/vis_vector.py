import matplotlib.pyplot as plt
from toolkit import variables
import os.path

def generateImageDistribution(docsOrdened, fechasThemes, muestraPmid):
    for ind in range(0, len(docsOrdened)):
        plt.figure()
        if fechasThemes == None:
            plt.plot(docsOrdened[ind])
        else:
            plt.plot(fechasThemes, docsOrdened[ind])

        pathDistributionSave = os.path.join(variables.TEST_RESOURCE, 'imageDistrib/')
        plt.savefig(pathDistributionSave + str(muestraPmid[ind]) + '.png')
        plt.close()
'''

fnameOb = open('C:/Users/rbrto/Documents/citation_lda/src/theme_discovery/fileToVis.csv')
#fnameOb = csv.reader(fnameOb,delimiter=",")
# test 5; single subplot
#plt.figure(figsize=(100,100))

first_line = fnameOb.readline()
encabezado = first_line.strip().split(", ")


fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 50
fig_size[1] = 12
plt.rcParams["figure.figsize"] = fig_size

#docs = ['18391392', '19129600', '28030437', '26484550', '21123889', '22760170', '18391373', '26484558']
#plt.plotfile(fnameOb, ('date', '18391392', '19129600', '28030437', '26484550', '21123889', '22760170', '18391373', '26484558'), subplots=False)
#plt.savefig('C:/Users/rbrto/Desktop/res_clda/total.png')
#
#
for doc in encabezado:
    if doc == 'date':
        continue
    else:
        plt.plotfile(open('C:/Users/rbrto/Documents/citation_lda/src/theme_discovery/fileToVis.csv'), ('date', str(doc)), subplots=False)
        plt.savefig('C:/Users/rbrto/Desktop/res_clda/'+str(doc)+'.png')


'''

