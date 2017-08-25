'''
Created on Feb 16, 2013

@author: xwang95
'''

class Graph(object):
    '''
    classdocs
    '''
    edges = None;
    nodes = None;
    directed = None;
    
    def __init__(self, directed=True):
        '''
        Constructor
        '''
        self.nodes = {};
        self.edges = {};
        self.directed = directed;
        return;
    
    def addNode(self, nId):
        if(nId not in self.nodes): self.nodes[nId] = {};
        return;
    
    def addEdge(self, beg, end, wet=1.0):
        self.addNode(beg);
        self.addNode(end);    
        if(self.directed):
            if(beg not in self.edges): self.edges[beg] = {};
            if(end not in self.edges[beg]): self.edges[beg][end] = self.edges[beg].get(end, 0.0) + wet;
        else:
            if(beg not in self.edges): self.edges[beg] = {};
            if(end not in self.edges): self.edges[end] = {};
            if(end not in self.edges[beg]): self.edges[beg][end] = self.edges[beg].get(end, 0.0) + wet;
            if(beg not in self.edges[end]): self.edges[end][beg] = self.edges[end].get(beg, 0.0) + wet;
        return;