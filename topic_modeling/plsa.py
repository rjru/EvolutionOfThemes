'''
Created on Mar 26, 2012

@author: xiaolong
'''
from copy import deepcopy
import random
import math
from pydoc import Doc, doc
import sys
'''implementation'''

class PLSA:
    D = 0;
    W = 0;
    K = 0;
    
    ObsDW = None;
    
    vocabulary = [];
    dictionary = {};
    p_z = [];
    p_d_z = [];
    p_w_z = [];
    norm_w_d = [];
    n_w_d = {};
    avgLen = 0;
    iterNum = 0;
    epsilon = 0.0001;
    w_d_pair = set();
    maxIterNum = 200
    
    def insertDWC(self, d, w, c):
        if(d not in self.n_w_d): self.n_w_d[d] = {};
        if(w not in self.n_w_d[d]): self.n_w_d[d][w] = 0.0;
        self.n_w_d[d][w] += c;
        self.w_d_pair.add((d, w));
        
    def __init__(self, data, D, W, K, maxIterNum, withheld=0.3):
        print "[PLSA]: Initialization";
        self.D = D;
        self.W = W;
        self.K = K;
        self.maxIterNum = maxIterNum;
        self.n_w_d = {};
        self.w_d_pair = set();
        totalWordCnt = 0;
        '''documents count n_w_d'''
        print("[PLSA]: Reading Data, document counts n_w_d");        
        for v in data:
            d = v[0];
            w = v[1];
            c = v[2];
            self.insertDWC(d, w, c);
            totalWordCnt += c;
        self.avgLen = float(totalWordCnt) / float(self.D);  # average document length

        print("[PLSA]: Initialize p(z) (uniform distributed), p_z");
        self.p_z = [1.0 / float(self.K) for x in range(self.K)];  # p_z added
        print("[PLSA]: Initialize p(d|z), sparse initialized, p_d_z");
        for i in range(self.K):
            if(i < self.D): 
                vec = [withheld / ((self.D) - 1) for x in range(self.D)];
                vec[i] = 1.0 - withheld;
            else:  # this should not be executed for general use with (topicNum<docNum)
                vec = [random.random() for x in range(self.D)];
                vec = [float(x) / sum(vec) for x in vec];  # random vec for p_d_z
            self.p_d_z.append(vec);  # p_z_d added (vec)
#===============================================================================
# DEBUG:
#           if(sum(vec) != 1.0): print '*********%f*********' % sum(vec);
#===============================================================================
        print "[PLSA]: Initialize p(w|z), p_w_z";
        for i in range(self.zNum):
            fVec = [0.0 for x in range(self.W)];
            s = 0;
            doc = [0.0 for w in self.W];
            if(i < self.D): 
                doc = [self.n_w_d[i].get(w, 0.0) for w in self.W];
                s = float(sum(doc));  # total word count in doc
            else:  # this should not be executed for general use with (topicNum<docNum)
                for i in range(int(self.avgLen)):
                    w = int(random.random() * self.W);
                    doc[w] += 1.0;
                s = float(int(self.avgLen));
            for idx in self.W: fVec[idx] += doc[idx] * (1 - withheld) / s;  # fVec: p_w_z
            for idx in self.W: fVec[idx] += withheld / self.W;
#===============================================================================
# DEBUG:
#            if(sum(fVec) != 1.0): print '*********%f*********' % sum(fVec);
#===============================================================================
            self.p_w_z.append(fVec);
            
    '''p(z) * p(d|z) * p(w|z)'''
    def curJntProb(self, z, d, w):
        return float(self.p_z[z] * self.p_d_z[z][d] * self.p_w_z[z][w]);

    '''posterior probability of p(z|w,d) using current model'''
    def posteriorProb(self, z, d, w): return self.curJntProb(z, d, w) / self.norm_w_d[(d, w)];
        
    '''normalization term of P(z|w,d)'''
    def Estep(self):
        self.norm_w_d = {};
        for (d, w) in self.w_d_pair: self.norm_w_d[(d, w)] = sum([self.curJntProb(z, d, w) for z in range(self.K)]);
        return;
    
    '''updating the model'''
    def Mstep(self):
        new_p_z = [0.0 for z in range(self.K)];
        new_p_d_z = [[0.0 for d in range(self.D)] for z in range(self.K)];
        new_p_w_z = [[0.0 for w in range(self.W)] for z in range(self.K)];
        '''computing unnormalized p(z)'''
        for z in range(self.K):
            for (d, w) in self.w_d_pair:
                val = self.posteriorProb(z, d, w) * self.n_w_d[d][w];
                new_p_z[z] += val;
                new_p_d_z[z][d] += val;
                new_p_w_z[z][w] += val;
        '''normalizing'''
        new_p_z = map(lambda x: x / sum(new_p_z), new_p_z);
        for z in range(self.K): 
            new_p_d_z[z] = map(lambda x: x / sum(new_p_d_z[z]), new_p_d_z[z]);
            new_p_w_z[z] = map(lambda x: x / sum(new_p_w_z[z]), new_p_w_z[z]);
        '''updating'''
        self.p_z = new_p_z;
        self.p_d_z = new_p_d_z;
        self.p_w_z = new_p_w_z;
        return;
        
    '''Combination of Estep and Mstep'''
    def Iter(self):
        print("[PLSA]: E-step for Iter: {0}".format(self.iterNum));
        self.Estep();
        print("[PLSA]: M-step for Iter: {0}".format(self.iterNum));
        self.Mstep();
        self.iterNum += 1;
    
    '''Check the loglikelihood'''
    def LogLikelihood(self):
        ll = 0.0;
        for (d, w) in self.w_d_pair:
            val = sum([self.curJntProb(z, d, w) for z in self.K]);
            ll += math.log(val) * self.n_w_d[d][w];                        
        return ll;
        
    '''perform the PLSA algorithm'''
    def perform(self):
        print("[PLSA]: Entering PLSA Modeling");
        ll = -99999999.9;
        prog = 0.0;
        mil = 0.0;
        step = 0.05;
        for t in range(self.maxIterNum):
            self.Iter();
            prog = float(t) / self.maxIterNum;
            if(prog >= mil):
                mil += step;
                new_ll = self.LogLikelihood();
                print("[PLSA]: LogLikelihood Optimized from\t{0:.6f} to \t{1:.6f}".format(ll, new_ll));
                if(new_ll <= ll + self.epsilon): break;
                ll = new_ll;
        print "[PLSA]: termination";
#===============================================================================
# DEBUG:
#        print len(self.p_w_z);
#        for z in range(self.zNum):
#            print len(self.p_w_z[z]);
#            print self.p_w_z[z][1:10];
#        #CHECK
#        if(abs(sum(self.p_z) - 1) > self.epsilon): 
#            print "p(z): %f" % sum(self.p_z);
#        for z in range(self.zNum):
#            if(abs(sum(self.p_d_z[z]) - 1) > self.epsilon):
#                print "p(d|z): %f" % sum(self.p_d_z[z]);
#        for z in range(self.zNum):
#            if(abs(sum(self.p_w_z[z]) - 1) > self.epsilon):
#                print "p(w|z): %f" % sum(self.p_w_z[z]);
#===============================================================================
        topicWeights = self.p_z;
        topicDocDist = self.p_d_z;
        topicWrdDist = self.p_w_z;
        return (topicWeights, topicDocDist, topicWrdDist);        
    
if(__name__ == "__main__"):
    pass;
