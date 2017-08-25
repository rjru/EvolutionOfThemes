'''
Created on Feb 18, 2013

@author: xwang95
'''
import sys

colorDict = {}
    
def enable():
    global colorDict;
    colorDict['header'] = '\033[95m';
    colorDict['okblue'] = '\033[94m';
    colorDict['okgreen'] = '\033[92m';
    colorDict['warning'] = '\033[93m';
    colorDict['fail'] = '\033[91m';
    colorDict['endc'] = '\033[0m';
    colorDict['blue'] = '\033[34m';
    colorDict['green'] = '\033[32m';
    colorDict['cyan'] = '\033[36m';
    colorDict['red'] = '\033[31m';
    colorDict['purple'] = '\033[35m';
    colorDict['brown'] = '\033[33m';
    colorDict['white'] = '\033[1;37m';
    return;

def disable(self):
    global colorDict;
    for k in colorDict: colorDict[k] = '';
            
def toString(s, color='warning'):
    if color not in colorDict: color = 'warning';
    return colorDict[color] + str(s) + colorDict['endc'];

def cPrint(s, color='warning'):
    sys.stdout.write(toString(s, color));
    sys.stdout.flush();

enable();

if __name__ == '__main__':
    pass
