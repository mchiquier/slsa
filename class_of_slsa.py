# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:28:22 2017

@author: mchiquier
"""

from numpy import zeros, asarray, transpose, sum,  diag, dot, arccos
from numpy.linalg import norm
#import numpy
from scipy.linalg import svd, inv

from slsa import superpersona_pertheme
from slsa import titlespertheme_list
#import re, random, pylab
from math import pi, log
#from operator import itemgetter
#from pattern.web import URL, Document, plaintext

# stopwords, retreived from http://www.lextek.com/manuals/onix/stopwords1.html

stopwords = ['a', 'about']
ignore_characters = ''',:'!'''


class LSA(object):
    def __init__(self, stopwords, ignore_characters):
        self.stopwords = stopwords
        self.ignore_characters = ignore_characters
        self.wdict = {}
        self.dcount = 0        
    def parse(self, doc):
        words = doc.split();
        for w in words:
            w = w.lower()
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1      
    def build(self): # Create count matrix
        self.keys = [k for k in self.wdict.keys()]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
    
    def findincommon(self,newdoc):
        words = newdoc.split()
        self.newvec = []
        for w in self.wdict:
            w=w.lower()
            if w in words:
                self.newvec.append(1)
            else: 
                self.newvec.append(0)
    
    def calc(self): # execute SVD
        self.U, self.S, self.Vt = svd(self.A, full_matrices =False)
    def TFIDF(self): # calculate tfidf score
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])
    def returnS(self):
        return self.S
    def returnU(self):
        return -1 * self.U
    def returnNewvec(self):
        return self.newvec   
    def returnVt(self):
        return -1 * self.Vt
    def printSVD(self):
        print 'Singular values: '
        print self.S
        print 'U matrix: '
        print -1*self.U[:, 0:3]
        print 'Vt matrix: '
        print -1*self.Vt[0:3, :]

import numpy as np
def projectnewdoc(query1, docs, eigs): # core comparison function. 
    hello = LSA(stopwords, ignore_characters)
    query1 = superpersona_pertheme['Banca']
    docs = titlespertheme_list
    for q in docs:
        hello.parse(q)
    hello.build()
    hello.calc()
    hello.findincommon(query1)
    newvec = hello.returnNewvec()
    newvec = np.matrix(newvec)
    U = hello.returnU()
    S = hello.returnS()
    S[list(eigs)] = 0
    S = diag(hello.S)
    vector_projected =(dot(newvec, U))*np.linalg.pinv(S)
    return vector_projected

def whichisclosest(query, docs): 
    lsa = LSA(stopwords, ignore_characters)
    for q in docs:
        lsa.parse(q)
    lsa.build()
    lsa.calc()
    Vt = lsa.Vt
    vectors =[dot(query,Vt[:,i]) for i in range(len(Vt))]
    whichdoc_index = vectors.index(max(vectors))
    difference = 1-max(vectors)
    return whichdoc_index, difference

#for every permutation, check the difference per doc and sum them
#which eigenvalues give the lowest sum?
import itertools
indeces = range(0,20)
listofcombos = list(itertools.combinations(indeces, 3))
thebest = 100000
besteigs = [0,0,0]
for each in listofcombos:
    for person in superpersona_pertheme : 
        sumresult = 0
        newvector = projectnewdoc(person, titlespertheme_list, each)
        a,b = whichisclosest(newvector, titlespertheme_list)
        sumresult = sumresult + b
        if sumresult < thebest:
            thebest = sumresult
            best_eigs = each

