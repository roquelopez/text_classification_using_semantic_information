# -*- coding: utf-8 -*-
'''
Created on 22/07/2013

@author: roque
'''

import os
import utils

class TextGraph(object):

    def __init__(self, keywords_list, windows=5):
        self.__windows = windows
        self.__keywords_list = keywords_list
        self.__vertices = list()
        self.__edges = [None] * len(keywords_list) 

        for k in range(len(keywords_list)):
            self.__edges[k] = [None] * len(keywords_list)

    def create_text_graph(self, folder_path):
        self.__create_vertices()

        for name_document in os.listdir(folder_path):
            text_document = utils.read_file(os.path.join(folder_path, name_document))
            self.__create_edges(text_document)
    
    def __create_vertices(self):
        for keyword in self.__keywords_list.keys():
            self.__vertices.append(keyword)      

    def __create_edges(self, text_document):
        keywords_positions = self.__get_keywords_positions(text_document)

        for i in range(len(self.__vertices)):
            if self.__vertices[i] in keywords_positions:
                for j in range(i+1, len(self.__vertices)):
                    if self.__vertices[j] in keywords_positions:
                        if self.__is_in_windows(keywords_positions[self.__vertices[i]], keywords_positions[self.__vertices[j]]):
                            if self.__edges[i][j] is None:
                                self.__edges[i][j] = 0
                                self.__edges[j][i] = 0
                            self.__edges[i][j] += 1
                            self.__edges[j][i] += 1
                        
    def __get_keywords_positions(self, text_document):
        word_list = utils.get_words(text_document)
        position_list = dict()
        for i in range(len(word_list)):
            if word_list[i] in self.__keywords_list:
                if not word_list[i] in position_list:
                    position_list[word_list[i]] = list()
                position_list[word_list[i]].append(i)
        return position_list

    def __is_in_windows(self, position_list1, position_list2): 
        for pos1 in position_list1:
            for pos2 in position_list2:
                if abs(pos1 - pos2) < self.__windows:
                    return True
        return False

    def get_edges(self):
        return self.__edges

    def get_vertices(self):
        return self.__vertices
  
    def print_text_graph(self):
        cont = 0
        for i in range(len(self.__vertices)):
            for j in range(i+1, len(self.__vertices)):
                if self.__edges [i][j] == 1:
                    cont += 1
        print(cont)

        for edge in self.__edges:
            print(edge)