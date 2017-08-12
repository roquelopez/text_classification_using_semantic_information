# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2013

@author: roque
'''

import urllib.request
import utils
from copy import deepcopy
from time import sleep

class SemanticRank(object):

    def __init__(self, edges, vertices):
        self.__edges = deepcopy(edges)
        self.__semantic_weigth = deepcopy(edges)
        self.__vertices = vertices
        self.__size = len(edges)       
        self.__outlink = [0] * self.__size 
        self.__alpha = 0.5
        self.__iterations = 10
        self.__ohsumed_weights = utils.semantic_weights("../resource/ohsumed_weights.txt")

    def rank(self):
        self.__get_semantic_weigths()
        count = 0
        tmp_ranking = [0] * self.__size 
        ranking = [1] * self.__size

        for i in range(self.__size):
            for j in range(self.__size): 
                if self.__edges[i][j] is not None:
                    self.__outlink[i] = self.__outlink[i] + 1                  

        while count < self.__iterations:
            for i in range(self.__size):
                tmp_ranking[i] = ranking[i]
           
            for i in range(self.__size):
                sumatoria = 0
                for j in range(self.__size):
                    if self.__edges[j][i] is not None:
                        sumatoria += (tmp_ranking[j]/ self.__outlink[j])# semantic text graph
                        #sumatoria += (self.__edges[i][j] * (self.__semantic_weigth[i][j]) * tmp_ranking[j])/ self.__outlink[j]#using frequency
                ranking[i] = (1 - self.__alpha) + (self.__alpha * sumatoria)

            count += 1

        return ranking

    def get_ranking_list(self):
        ranking = self.rank()
        ranking_list = dict()
        for i in range(len(ranking)):
            ranking_list[self.__vertices[i]] = ranking[i]

        return ranking_list

    def __get_semantic_weigths(self):
        cont= 0

        for i in range(len(self.__edges)):
            for j in range(i+1, len(self.__edges)):
                if self.__edges[i][j] is not None:
                    cont += 1
                    similarity = self.__get_similarity(self.__vertices[i], self.__vertices[j])
                    self.__semantic_weigth[i][j] = similarity
                    self.__semantic_weigth[j][i] = similarity

    def __get_similarity(self, word1, word2, attemps=20):
        if word1+'_'+word2 in self.__ohsumed_weights:
            return self.__ohsumed_weights[word1+'_'+word2] 
        
        if word2+'_'+word1 in self.__ohsumed_weights:
            return self.__ohsumed_weights[word2+'_'+word1] 

        i = 0
        #url = "http://atlas.ahc.umn.edu/cgi-bin/umls_similarity.cgi?=word1"+word1+"&word2="+word2+"&sab=MSH&rel=PAR%2FCHD&similarity=path&button=Compute+Similarity&sabdef=UMLS_ALL&reldef=CUI%2FPAR%2FCHD%2FRB%2FRN&relatedness=vector"
        url = "http://atlas.ahc.umn.edu/cgi-bin/umls_similarity.cgi?word1="+word1+"&word2="+word2+"&sab=MSH&rel=PAR%2FCHD&similarity=path&sabdef=UMLS_ALL&reldef=CUI%2FPAR%2FCHD%2FRB%2FRN&relatedness=vector&button=Compute+Relatedness"
        fout = open("../resource/lexical/ohsumed_weights.txt", 'a')
        while i < attemps:
            try:
                conexion = urllib.request.urlopen(url)
                break
            except Exception as e:
                print(e)
                i += 1
                sleep(10 * i)
        text = str(conexion.read())
        pattern = ["using Vector Measure (vector) is", ".</p>"]
        index = text.find(pattern[0])
        similarity = -1000#1.0
        if index > 0:
                index = index + len(pattern[0])
                index2 = text[index:].find(pattern[1])
                similarity = float(text[index:index + index2]) #+ 1.0

        fout.write(" %s %s %s\n" % (word1, word2, similarity))
        fout.close()
        conexion.close()
        return similarity

    def __get_similarity_porter(self, word1, word2):
        for key, value in self.__ohsumed_weights.items():
            tmp = key.split('_')
            if tmp[0].startswith(word1) and tmp[1].startswith(word2):
                return value
            elif tmp[0].startswith(word2) and tmp[1].startswith(word1):
                return value

        return 1.0