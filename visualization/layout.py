from visualization.tree import *
import math
import numpy as np
from toolkit.utility import *

def postorder_traversal(v):
    if v.getDeg() == 1:
        v.setNumLeavesSubTree(1)
    else:
        v.setNumLeavesSubTree(0)

        wr = v.getRightChild()
        if wr != None:
            postorder_traversal(wr)
            v.setNumLeavesSubTree(v.getNumLeavesSubTree() + wr.getNumLeavesSubTree())

        wl = v.getLeftChild()
        if wl != None:
            postorder_traversal(wl)
            v.setNumLeavesSubTree(v.getNumLeavesSubTree() + wl.getNumLeavesSubTree())

def preorder_traversal(v, l_root):
    if v.getParent() != None:  # significa que no es la raiz
        u = v.getParent()
        #tuple(2*np.array(set1))
        temp1 = tuple(v.getweightAristToParentVal() * np.array((math.cos(math.radians(v.getT() + v.getW()/2)), math.sin(math.radians(v.getT() + v.getW()/2)))))
        temp2 = u.getX()
        v.setX((temp1[0]+temp2[0], temp1[1]+temp2[1]))
    en = v.getT()

    wr = v.getRightChild()
    if wr != None:
        wr.setW((wr.getNumLeavesSubTree()/l_root) * 360)
        wr.setT(en)
        en = en + wr.getW()
        preorder_traversal(wr, l_root)

    wl = v.getLeftChild()
    if wl != None:
        wl.setW((wl.getNumLeavesSubTree()/l_root) * 360)
        wl.setT(en)
        en = en + wl.getW()
        preorder_traversal(wl, l_root)

def radialLayout(rtree):
    print('hello radial layout')
    postorder_traversal(rtree)
    rtree.setX((0, 0))
    rtree.setW(360)
    rtree.setT(0)

    l_root = rtree.getNumLeavesSubTree()  # esto es si el nodo es el root
    preorder_traversal(rtree, l_root)
    print('hello tree')

def preorder(tree):
    if tree:
        print(tree.getRootVal(), "deg: ", tree.getDeg(), " leaves: ", tree.getNumLeavesSubTree(), ' W: ', tree.getW(), ' T:', tree.getT(), ' X: ', tree.getX())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())

if __name__ == '__main__':
    # inicializate tree
    rootedTree = BinaryTree('a')
    rootedTree.insertLeft('b', 2)
    rootedTree.getLeftChild().insertRight('d', 4)
    rootedTree.getLeftChild().insertLeft('g', 8)
    rootedTree.insertRight('c', 3)
    rootedTree.getRightChild().insertLeft('e', 5)
    rootedTree.getRightChild().insertRight('f', 2)

    #print(rootedTree.getRootVal())
    radialLayout(rootedTree)
    preorder(rootedTree)

    #aaa = newick_to_pairwise_nodes('((((H,K)D,(F,I)G)B,E)A,((L,(N,Q)O)J,(P,S)M)C);')