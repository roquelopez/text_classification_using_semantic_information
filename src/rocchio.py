# -*- coding: utf-8 -*-
'''
Created on 23/09/2013

@author: roque
'''

import os
import utils
from math import pow, sqrt, log

class Rocchio(object):

    def __init__(self):
        self.__classes = dict()

    def train(self, folder_path):
        for class_id in os.listdir(folder_path):
            class_path = os.path.join(folder_path, class_id)
            if os.path.isdir(class_path):
                self.__classes[class_id] = dict()
                self.__read_documents(class_id, class_path)
        self.__tfidf()

    def __tfidf(self):
        N_classes = len(self.__classes)
        for id_class, words  in self.__classes.items():
            for word in words:
                Ni_classes = self.__get_nro_classes(word)
                self.__classes[id_class][word] *=  log( N_classes / Ni_classes )

    def __get_nro_classes(self, word):
        cont = 0

        for words in self.__classes.values():
            if word in words:
                cont += 1

        return cont

    def __read_documents(self, id_class, class_path):
        size = len(os.listdir(class_path))
        for name_document in os.listdir(class_path):
            text_document = utils.read_file(os.path.join(class_path, name_document))
            word_list = utils.get_words(text_document)

            for word in word_list:
                if word in self.__classes[id_class]:
                    self.__classes[id_class][word] += 1
                else:
                    self.__classes[id_class][word] =  1

        for key in self.__classes[id_class].keys():
            self.__classes[id_class][key] /= size

    def test(self, folder_path):
        correct_answers = 0
        total = 0
        for class_id in os.listdir(folder_path):
            for name_document in os.listdir(os.path.join(folder_path, class_id)):
                text_document = utils.read_file(os.path.join(folder_path, class_id, name_document))
                if self.__evaluate(text_document, class_id):
                    correct_answers += 1 
                total += 1 
        print("Result: %s of %s ==> %s %%" % (correct_answers, total, correct_answers * 100 / total))

    def __evaluate(self, text_document, class_id):
        vector_document = self.__get_frequency_word(text_document)
        similarities = dict()
        for id_class, vector_class in self.__classes.items():
            similarities[id_class] = self.__euclidian(vector_class, vector_document)

        sorted_list = sorted(similarities.items(), key=lambda x:x[1])

        if class_id == sorted_list[0][0]:
            return True
        return False

    def __get_frequency_word(self, text_document):
        word_list = utils.get_words(text_document)
        frequency_word = dict()
        for word in word_list:
            if word in frequency_word:
                frequency_word[word] += 1
            else:
                frequency_word[word] = 1
        return frequency_word

    def __euclidian(self, vector1, vector2):
        tmp_total = 0
        for word in vector1.keys():
            value = vector2[word] if word in vector2 else 0.0
            tmp_total +=  pow(vector1[word] - value, 2) 

        for word in vector2.keys():
            if not word in vector1:
                tmp_total +=  pow(vector2[word] - 0.0, 2) 

        return sqrt(tmp_total)  