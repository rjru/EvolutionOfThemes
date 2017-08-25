'''
Created on Feb 13, 2013

@author: xwang95
'''
class GexfGen(object):
    strGraph = "";
    indent = "";
    curIndent = "";
    isDirected = True;
    
    attToId = {};
    attToType = {};
    idToAtt = {};
    nodeToId = {};
    idToNode = {};
    nodes = {};
    edges = [];
    
    def increaseCurrentIndent(self):
        self.curIndent = "  " + self.curIndent;
        return;
    
    def decreaseCurrentIndent(self):
        if(self.curIndent >= 2): self.curIndent = self.curIndent[2:];
        return;
    
    def __init__(self, isDirected=True):
        self.strGraph = "";
        self.indent = "  ";
        self.curIndent = "";
        self.attToId = {};
        self.attToType = {};
        self.idToAtt = {};
        self.nodeToId = {};
        self.idToNode = {};
        self.nodes = {};
        self.edges = [];
        self.isDirected = isDirected;
        return;
    
    def addIndentToStrLst(self, strLst):
        return [self.indent + s for s in strLst];
    
    def regNode(self, node):
        if(node not in self.nodeToId):
            id = len(self.nodeToId);
            self.nodeToId[node] = id;
            self.idToNode[id] = node;
            self.nodes[node] = {};
        return;
    
    def regAtt(self, att, type):
        if(att not in self.attToId):
            id = len(self.attToId);
            self.attToId[att] = id;
            self.idToAtt[id] = att;
            self.attToType[att] = type;
        return;
    
    def addNodeAtt(self, node, att, value, type):
        self.regNode(node);
        self.regAtt(att, type);
        self.nodes[node][att] = value;
        return;
    
    def addEdge(self, sourceNode, targetNode, weight):
        self.edges.append((sourceNode, targetNode, weight));
        return;
    
    def getNodeStrLst(self, nodeIdx):
        nodeStrLst = [];
        if(len(self.nodes[self.idToNode[nodeIdx]]) == 0): return ['<node id="{0}" label="{1}" />'.format(nodeIdx, self.idToNode[nodeIdx])];
        nodeStrLst.append('<node id="{0}" label="{1}">'.format(nodeIdx, self.idToNode[nodeIdx]));
        nodeStrLst.append(self.indent + '<attvalues>');
        for att in self.nodes[self.idToNode[nodeIdx]]:
            attId = self.attToId[att];
            val = self.nodes[self.idToNode[nodeIdx]][att];
            nodeStrLst.append(self.indent + self.indent + '<attvalue for="{0}" value="{1}"/>'.format(attId, val));
        nodeStrLst.append(self.indent + '</attvalues>');    
        nodeStrLst.append('</node>');
        return nodeStrLst;
    
    def getEdgeStr(self, edgeIdx):
        (sourceNode, targetNode, weight) = self.edges[edgeIdx];
        sourceNodeId = self.nodeToId[sourceNode];
        targetNodeId = self.nodeToId[targetNode];
        return '<edge id="{0}" source="{1}" target="{2}" weight="{3}"/>'.format(edgeIdx, sourceNodeId, targetNodeId, weight);
    
    
    def getGraphStr(self):
        strGraphLst = [];
        strGraphLst.append('<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" xmlns="http://www.gexf.net/1.1draft" version="1.1">');
        if(self.isDirected): mode = "directed";
        else: mode = "undirected";
        strGraphLst.append(self.indent + '<graph mode="static" defaultedgetype="{0}">'.format(mode));
        attStrLst = [];
        attStrLst.append('<attributes class="node" mode="static">');
        for i in range(len(self.attToId)): attStrLst.append(self.indent + '<attribute id="{0}" title="{1}" type="{2}"/>'.format(i, self.idToAtt[i], self.attToType[self.idToAtt[i]]));
        attStrLst.append('</attributes>');
        nodesStrLst = [];
        nodesStrLst.append('<nodes>');
        for i in range(len(self.nodes)): nodesStrLst.extend(self.addIndentToStrLst(self.getNodeStrLst(i)));
        nodesStrLst.append('</nodes>');
        edgesStrLst = [];
        edgesStrLst.append('<edges>');
        for i in range(len(self.edges)): edgesStrLst.append(self.indent + self.getEdgeStr(i));
        edgesStrLst.append('</edges>');
        strGraphLst.extend(self.addIndentToStrLst(self.addIndentToStrLst(attStrLst)));
        strGraphLst.extend(self.addIndentToStrLst(self.addIndentToStrLst(nodesStrLst)));
        strGraphLst.extend(self.addIndentToStrLst(self.addIndentToStrLst(edgesStrLst))); 
        strGraphLst.append(self.indent + '</graph>');
        strGraphLst.append('</gexf>');
        self.strGraph = '\n'.join(strGraphLst); 
        return self.strGraph; 
        
if __name__ == '__main__':
    gexfGen = GexfGen();
    gexfGen.addNodeAtt(1, "food", "banana", "string");
    gexfGen.addNodeAtt(2, "food", "apple", "string");
    gexfGen.addNodeAtt(1, "drink", "coke", "string");
    gexfGen.addNodeAtt(2, "drink", "coke", "string");
    gexfGen.regNode(3);
    gexfGen.addEdge(1, 3, 0.5)
    print (gexfGen.getGraphStr());
    pass
