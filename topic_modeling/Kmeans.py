'''
Created on Oct 23, 2012

@author: xiaolong
'''
import math;
import random;
import sys;

class Kmeans(object):
    data = {}; #dictionary of dictionary
    topics = []; #list of dictionary
    topicPop = [];
    topicNormSquare = [];
    #The final latent labels assignment are resotred in labels (dictionary)
    #Kay - Data Index
    #Value - Latent Variable
    labels = {};
    K = 0;

    #Set the cluster/topic number
    def __init__(self, topicNum):
        self.K = topicNum;
        for k in range(0, topicNum):
            self.topics.append({});
            self.topicPop.append(0.0);
            self.topicNormSquare.append(0.0);
    
    #Use this to insert a feature f into data indexed by datIdx.
    #Insert f once increase the f value 1
    def insertFeature(self, datIdx, f):
        if(datIdx not in self.data): 
            self.data[datIdx] = {};
            k = random.randint(0, self.K - 1);
            self.topicPop[k] += 1.0;
            self.labels[datIdx] = k;
        
        k = self.labels[datIdx];
        self.data[datIdx][f] = self.data[datIdx].get(f, 0) + 1.0;
        self.topics[k][f] = self.topics[k].get(f, 0.0) + 1.0;
        self.topicNormSquare[k] += 2 * self.topics[k][f] - 1.0;        

    def cosCoef(self, feaVec1, topicId):
        v1 = feaVec1;
        v2 = self.topics[topicId];
        norm1 = math.sqrt(sum([x * x for x in v1.values()]));
        norm2 = math.sqrt(self.topicNormSquare[topicId]) / self.topicPop[topicId];
        
        x = sum([v1[k] * (v2[k] / self.topicPop[topicId]) for k in v1 if k in v2]) / (norm1 * norm2); 
        return x;
    
    def update(self, feaVec, k):
        scores = [self.cosCoef(feaVec, topicId) for topicId in range(0, self.K)];
        newK = scores.index(max(scores));
        if(k == newK): return newK;
    
        self.topicPop[k] -= 1.0;
        for f, v in feaVec.items(): 
            self.topics[k][f] = self.topics[k].get(f, 0.0) - v;
            self.topicNormSquare[k] -= 2 * self.topics[k][f] + 1.0;
        
        self.topicPop[newK] += 1.0;
        for f, v in feaVec.items(): 
            self.topics[newK][f] = self.topics[newK].get(f, 0.0) + v;
            self.topicNormSquare[newK] += 2 * self.topics[newK][f] - 1.0;
        return newK;

    def iteration(self):
        updateNum = 0.0;
        for datIdx in self.data:
            feaVec = self.data[datIdx];
            k = self.labels[datIdx];
            newK = self.update(feaVec, k);
            self.labels[datIdx] = newK;
            if(newK != k): updateNum += 1.0;
        updateRatio = updateNum / float(len(self.data));
        return updateRatio;
    
    #Use this function to perform K-Means iterations
    def compute(self):
        #initialization
        for k in range(0, self.K): 
            for f in self.topics[k]:
                self.topics[k][f] /= self.topicPop[k];
        iter = 0;
        
        while(True):
            updateRatio = self.iteration();
            print(str(iter) + ':\t' + str(updateRatio));
            iter += 1;
            if(updateRatio <= 2e-4): break;
        topics = [[] for k in range(0, self.K)];
        for k, v in self.labels.items(): topics[v].append(k);
        return topics;
