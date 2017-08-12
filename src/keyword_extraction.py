# -*- coding: utf-8 -*-
'''
Created on 17/07/2013

@author: roque
'''

import os
import utils
import nltk
from math import log

class KeywordExtraction(object):

    def __init__(self):
        self.__classes = dict()
        self.__keywords_weigth = dict()

    def create_class(self, folder_path):
        for sub_folder in os.listdir(folder_path):
            sf_path = os.path.join(folder_path, sub_folder)
            if os.path.isdir(sf_path):
                self.__classes[sub_folder] = dict()
                self.__read_documents(sub_folder, sf_path)

    def __read_documents(self, id_class, class_path):
        for name_document in os.listdir(class_path):
            text_document = utils.read_file(os.path.join(class_path, name_document))
            self.__fill_class(id_class, name_document, text_document)

    def __fill_class(self, id_class, name_document, text_document):
        word_list = utils.get_words(text_document)

        for word in word_list:
            tag = nltk.pos_tag([word])
            if tag[0][1].startswith('N') or tag[0][1].startswith('V') or tag[0][1].startswith('S') or tag[0][1].startswith('F') or tag[0][1].startswith('J'):
                if word in self.__classes[id_class]:
                    if name_document in self.__classes[id_class][word]:
                        self.__classes[id_class][word][name_document] += 1
                    else:
                        self.__classes[id_class][word][name_document] =  1
                else:
                    self.__classes[id_class][word] =  dict()
                    self.__classes[id_class][word][name_document] =  1

    def __calculate_weigths(self):
        N_classes = len(self.__classes)
        for id_class in self.__classes:
            self.__keywords_weigth[id_class] = dict()
            for word in self.__classes[id_class]:
                DFi  = self.__get_word_in_documentclass(word, id_class)
                Ni_classes = self.__get_word_in_classes(word)
                weigth = DFi * log( N_classes / Ni_classes, 10)
                self.__keywords_weigth[id_class][word] = weigth

    def extract_keywords(self, top, folder_path):
        self.__calculate_weigths() 
        tmp_list = dict()
        for id_class in self.__classes:
            print(id_class)
            keywords_top = dict()
            sorted_list = sorted(self.__keywords_weigth[id_class].items(), key=lambda x:x[1], reverse=True)

            for document_name in os.listdir(os.path.join(folder_path, id_class)):
                i = 0
                cont = 0
                while cont < top and i < len(sorted_list):
                    word = sorted_list[i][0]
                    if document_name in self.__classes[id_class][word] and len(word) > 2 and word !="patient":
                        keywords_top[word] = sorted_list[i][1]
                        cont += 1
                    i += 1
            tmp_list[id_class] = keywords_top

        return tmp_list 

    def __get_word_in_classes(self, word):
        cont = 0
        for words in self.__classes.values():
            if word in words:
                cont += 1
        return cont

    def __get_word_in_documentclass(self, word, id_class):
        return len(self.__classes[id_class][word])

    def __print_words(self):
        for words in self.__classes.values():
            print(words)