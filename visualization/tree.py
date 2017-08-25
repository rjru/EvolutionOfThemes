
# http://interactivepython.org/runestone/static/pythonds/Trees/TreeTraversals.html


class BinaryTree:
    def __init__(self, rootObj, weightAristToParent = None, deg=0, parent=None, extraInformation = None):
        self.parent = parent
        self.key = rootObj
        self.deg = deg
        self.NumLeavesSubTree = 0
        self.X = None
        self.W = None
        self.T = None
        self.weightAristToParent = weightAristToParent
        self.leftChild = None
        self.rightChild = None
        self.root = None
        self.extraInformation = extraInformation

    def insertLeft(self, newNode, weightAristToParent, extraInformation=None):
        parent = self
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode, weightAristToParent, 1, parent, extraInformation)
            self.deg = self.deg + 1
        else:
            t = BinaryTree(newNode, weightAristToParent, 1, parent, extraInformation)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self, newNode, weightAristToParent, extraInformation=None):
        parent = self
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode, weightAristToParent, 1, parent, extraInformation)
            self.deg = self.deg + 1
        else:
            t = BinaryTree(newNode, weightAristToParent, 1, parent, extraInformation)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getDeg(self):
        return self.deg

    def getNumLeavesSubTree(self):
        return self.NumLeavesSubTree

    def setNumLeavesSubTree(self, val):
        self.NumLeavesSubTree = val

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self, obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def getweightAristToParentVal(self):
        return self.weightAristToParent

    def setX(self, val):
        self.X = val

    def setW(self, val):
        self.W = val

    def setT(self, val):
        self.T = val

    def getX(self):
        return self.X

    def getW(self):
        return self.W

    def getT(self):
        return self.T

    def getParent(self):
        return self.parent

    def getExtraInformation(self):
        return self.extraInformation


def preorder(tree):
    if tree:
        print(tree.getRootVal())
        preorder(tree.getLeftChild())
        preorder(tree.getRightChild())

def postorder(tree):
    if tree != None:
        postorder(tree.getLeftChild())
        postorder(tree.getRightChild())
        print(tree.getRootVal())

#def insertRecursive(tree, rootedTree, pubmedDocs, muestraPmid):
def insertRecursive(tree, rootedTree, metaDoc, metaTheme):
    if tree:  # arbol original
        lenChild = len(tree.get_children())
        if lenChild == 1:
            rootedTree.insertRight(tree.get_children()[0].name,
                                   tree.get_children()[0].dist,
                                   tree.get_children()[0].name if tree.get_children()[0].name in [str(i) for i in metaDoc["muestraPmid"]] else None)

            insertRecursive(tree.get_children()[0], rootedTree.getRightChild(), metaDoc, metaTheme)
        if lenChild == 2:
            #print(tree.get_children()[0].dist)
            rootedTree.insertRight(tree.get_children()[0].name,
                                   tree.get_children()[0].dist,
                                   tree.get_children()[0].name if tree.get_children()[0].name in [str(i) for i in metaDoc["muestraPmid"]] else None)

            rootedTree.insertLeft(tree.get_children()[1].name,
                                  tree.get_children()[1].dist,
                                  tree.get_children()[0].name if tree.get_children()[0].name in [str(i) for i in metaDoc["muestraPmid"]] else None)

            insertRecursive(tree.get_children()[0], rootedTree.getRightChild(), metaDoc, metaTheme)
            insertRecursive(tree.get_children()[1], rootedTree.getLeftChild(), metaDoc, metaTheme)

def setNamesTree(t):
    cont = 0
    for node in t.traverse("preorder"):
        # Do some analysis on node
        if node.name == '':
            node.name = 'i_root'
        if node.name == 'NoName':
            node.name = "i_" + node.name + '_' + str(cont)
        cont = cont + 1

#def EteTreeToBinaryTree(t, pubmedDocs, muestraPmid, themesDescript):
def EteTreeToBinaryTree(t, metaDoc, metaTheme):
    print('set Names')
    setNamesTree(t)
    # print("names:", t)
    print('insert recursive')
    rootedTree = BinaryTree(t.name,
                            extraInformation=metaDoc["pubmed"].docs[int(t.name)] if t.name in [str(i) for i in metaDoc["muestraPmid"]] else None)

    #insertRecursive(t, rootedTree, pubmedDocs, muestraPmid)
    insertRecursive(t, rootedTree, metaDoc, metaTheme)
    return rootedTree



'''
r = BinaryTree('a')
print(r.getRootVal())
print(r.getLeftChild())
r.insertLeft('b')
print(r.getLeftChild())
print(r.getLeftChild().getRootVal())


print(r.getRightChild())
print(r.getRightChild().getRootVal())
r.getRightChild().setRootVal('hello')
print(r.getRightChild().getRootVal())
print("borrarsh")
'''


r = BinaryTree('a')
r.insertLeft('b', 2)
r.getLeftChild().insertRight('d', 4)
r.insertRight('c', 3)
r.getRightChild().insertLeft('e', 5)
r.getRightChild().insertRight('f', 2)

print(r.getRightChild().getRootVal())
print(r.getRightChild().getweightAristToParentVal())

print('preorder')
preorder(r)
print('postorder')
postorder(r)
