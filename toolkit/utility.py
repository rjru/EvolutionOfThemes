'''
Created on Feb 1, 2013

@author: xwang95
'''
import random;
import os;
import os.path;
import sys;
import shutil;
import math;
from ete3 import Tree
import seaborn as sns

NOT_FOLD = True;
#===============================================================================
# Section: Topic Modeling
#===============================================================================
def getRankedIdxList(lst, reverseOption=False):
    return [idx for idx in sorted(range(len(lst)), key=lambda x: lst[x], reverse=reverseOption)];

def getRankedIdxMatrix(mtx, reverseOption=False):
    return [getRankedIdxList(lst, reverseOption) for lst in mtx];

def getDictRank(dict, key, reverse=False):
    rankToKey = {};
    keyToRank = {};
    for k in sorted(dict, key=key, reverse=reverse):
        r = len(rankToKey);
        rankToKey[r] = k;
        keyToRank[k] = r;
    return (rankToKey, keyToRank);

NOT_FOLD = True;
#===============================================================================
# parse
#===============================================================================
def parseNumVal(s):
    s = s.strip();
    try:
        v = int(s);
    except:
        try:
            v = float(s);
        except:
            v = 0;
    return v;

def parseYear(s):
    yearLst = [];
    cnt = 0;
    for i in range(len(s)):
        if('0' <= s[i] and s[i] <= '9'): cnt += 1;
        else: cnt = 0;
        if(cnt == 4): yearLst.append(parseNumVal(s[(i - 3):(i + 1)]));
    return yearLst;

NOT_FOLD = True;
#===============================================================================
# I/O
#===============================================================================
def readLines(num, reader):
    eof = False;
    lineLst = [reader.readline() for i in range(num)];
    if(not lineLst[num - 1]): eof = True;
    lineLst = [line.strip() for line in lineLst];
    return (lineLst, eof);

def readUntil(checkFunc, reader):
    eof = False;
    lineLst = [];
    while(True):
        lineLst.append(reader.readline());
        if(not lineLst[-1]):
            eof = True;
            break;
        if(checkFunc(lineLst[-1].strip())): break;
    lineLst = [line.strip() for line in lineLst];
    if(eof): lineLst = lineLst[:-1];  # no end of file line
    return (lineLst, eof);

def readChunk(reader): return readUntil(lambda x: (x == ""), reader);

def readMatrix(reader, row=None):
    lines = [];
    if(row is not None): (lines, eof) = readLines(row, reader);
    else: (lines, eof) = readUntil(lambda x: (x == ''), reader);
    return ([[parseNumVal(s) for s in line.split()] for line in lines], eof);

def readVector(reader):
    (lines, eof) = readLines(1, reader);
    if(not eof): return ([parseNumVal(s) for s in lines[0].split()], eof);
    else: return([], eof);

def printProgressBar(prog, step=0.04, addStr=""):
    prct = int(math.ceil(100 * prog));
    totlBlk = int(math.ceil(1.0 / step));
    progBlk = max(min(totlBlk, int(math.ceil(prog / step))) - 1, 0);
    futrBlk = max(totlBlk - progBlk - 1, 0);
    bar = '[' + ''.join(['=' for i in range(progBlk)]) + '>' + ''.join([' ' for i in range(futrBlk)]) + ']' + '({0})'.format(addStr);
    s = '\r[{0:>3}%]: {1}'.format(prct, bar);
    sys.stdout.write(s);
    sys.stdout.flush();
    return s;

def rFillSpaces(s, lineWidth=300):
    return str(s) + ''.join([' ' for i in range(lineWidth - len(s))]);

NOT_FOLD = True;
#===============================================================================
# string
#===============================================================================
def rmLeadingStr(s, srm):
    if(s.startswith(srm)): return s[len(srm):];
    return s;

def rmTrailingStr(s, srm):
    if(s.endswith(srm)): return s[:-len(srm)];

NOT_FOLD = True;
#===============================================================================
# file management
#===============================================================================
def removePath(path):
    if(not os.path.exists(path)): print('[remove_path@utility]: path not exist: {0}, Doing Nothing'.format(path));
    if(os.path.isdir(path)):
        print('[remove_path@utility]: removing directory: {0}'.format(path));
        shutil.rmtree(path);
    if(os.path.isfile(path)):
        print('removing files: {0}'.format(path));
        os.remove(path);
    return;

def mkDir(path):
    if(os.path.isdir(path)): print('[make_dir@utility]: path already exists as DIRECTORY! Doing Nothing');
    elif(os.path.isfile(path)): print('[make_dir@utility]: path already exist as FILE! Doing Nothing');
    else:
        print('[make_dir@utility]: make directory {0}'.format(path));
        os.makedirs(path);
    return;

NOT_FOLD = True;
#===============================================================================
# computing
#===============================================================================
def getVecNorm(vec, order): return math.pow(sum([math.pow(x, order) for x in vec]), 1.0 / order);

def normalizeVector(vec, order=None):
    if(order is not None): norm = getVecNorm(vec, order);
    else: norm = float(sum(vec));
    return [x / norm for x in vec];

def getDistExpectation(dist): return sum([k * dist[k] for k in dist]);

def getDistVariation(dist, expt=None):
    if(expt is None): expt = getDistExpectation(dist);
    return sum([((k - expt) ** 2) * dist[k] for k in dist]);

def getDistStd(dist, expt=None): return math.sqrt(getDistVariation(dist, expt));

def getMatrixVecMultiply(m, v): return [sum([vec[i] * v[i] for i in range(len(v))]) for vec in m];

def getTransposeSquareMatrix(m): return [[m[j][i] for j in range(len(m))] for i in range(len(m))];

def getVecSubstract(v1, v2): return [v1[i] - v2[i] for i in range(len(v1))];

#===============================================================================
# newick format
#===============================================================================
def newick_to_pairwise_nodes(newick_string):
    # we load a tree
    # ((((H,K)D,(F,I)G)B,E)A,((L,(N,Q)O)J,(P,S)M)C);
    # newick_string = newick_string + "i_root"
    t = Tree(newick_string, format=1)
    # t = t + "i_root"
    nodes = []
    edges = []
    dic_id = {}
    cont = 0

    for node in t.traverse("preorder"):
        # Do some analysis on node
        if node.name == '':
            node.name = 'i_root'

        if node.name == 'NoName':
            node.name = "i_" + node.name + '_' + str(cont)
            nodes.append({"id": cont, "name": node.name})
        else:
            nodes.append({"id": cont, "name": node.name})

        dic_id[node.name] = cont

        cont = cont + 1

    for node in t.traverse("preorder"):
        ancestor = ""
        # print (node.name)
        # print("antecesor")
        for anc in node.iter_ancestors():
            if anc:
                ancestor = anc
            break

        if ancestor != "":
            # print(ancestor.name, ", ", node.name, format(t.get_distance(ancestor, node),"f"))
            edges.append({"source": dic_id[ancestor.name], "target": dic_id[node.name],
                          "edgeWidth": format(t.get_distance(ancestor, node), "f")})

    json = {"nodes": nodes, "links": edges}
    return str(json).replace("'", '"')

# adecuacion del formato newick para utilizar el layout

def scale_colors(parts): # hace lo mismo que get_color_of_n pero usando una libreria
#http://seaborn.pydata.org/tutorial/color_palettes.html
    palette = sns.color_palette("Set2", parts) #cubehelix
    #palette = sns.cubehelix_palette(parts)
    #palette = sns.color_palette("Reds",parts) # esto es escala rgb del 0 al 1
    # aqui se convierte de 0 a 255
    palette_0_255 = []
    for color in palette:
        r = int(color[0]*255)
        g = int(color[1]*255)
        b = int(color[2]*255)
        palette_0_255.append((r, g, b))

    return palette_0_255

if __name__ == '__main__':
    pass