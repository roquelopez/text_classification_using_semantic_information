# -*- coding: utf-8 -*-
'''
Created on 18/07/2013

@author: roque
'''

import os
import utils
from math import pow, sqrt

class Classifier(object):

    def __init__(self, keywords_weigth):
        self.__keywords_weigth = keywords_weigth
        self.__confusion_matrix = dict()
        self.__no_documents = 0
        self.__correct_answers = 0
        self.__tp = dict()
        self.__fn = dict()
        self.__fp = dict()
        self.__elements = dict()
        self.__classes = list()

    def classify_all(self, folder_path):
        for sub_folder in os.listdir(folder_path):
            sf_path = os.path.join(folder_path, sub_folder)
            if os.path.isdir(sf_path):
                self.__read_documents(sub_folder, sf_path)
                self.__classes.append(sub_folder)
        print("Result: %s of %s ==> %s %%" % (self.__correct_answers, self.__no_documents, self.__correct_answers * 100 / self.__no_documents))

    def __read_documents(self, id_class, class_path):
        self.__confusion_matrix[id_class] = dict()
        self.__tp[id_class] = 0
        self.__fn[id_class] = 0
        document_list = os.listdir(class_path)
        self.__no_documents += len(document_list)
        self.__elements [id_class] = len(document_list)

        for name_document in document_list:
            text_document = utils.read_file(os.path.join(class_path, name_document))
            id_classification = self.__classify_document(text_document)

            if id_class == id_classification:
                self.__correct_answers += 1
                self.__tp[id_class] += 1
                if not id_class in self.__confusion_matrix[id_class]: self.__confusion_matrix[id_class][id_class] = 0
                self.__confusion_matrix[id_class][id_class] += 1
            else:
                self.__fn[id_class] += 1  
                if not id_classification in self.__fp: self.__fp[id_classification] = 0
                self.__fp[id_classification] += 1 
                if not id_classification in self.__confusion_matrix[id_class]: self.__confusion_matrix[id_class][id_classification] = 0
                self.__confusion_matrix[id_class][id_classification] += 1

    def __read_documents_k(self, id_class, class_path):
        self.__confusion_matrix[id_class] = dict()
        self.__tp[id_class] = 0
        self.__fn[id_class] = 0
        document_list = os.listdir(class_path)
        self.__no_documents += len(document_list)

        for name_document in document_list:
            text_document = utils.read_file(os.path.join(class_path, name_document))
            pissible_classification = self.__classify_document_euclidian(text_document)
            if id_class in pissible_classification:
                self.__correct_answers += 1

    def __classify_document(self, text_document):
        frequency_word = self.__frequency_word(text_document)
        similarity_list = dict()
        for class_id in self.__keywords_weigth:
            tmp_total = 0
            for keyword in self.__keywords_weigth[class_id]:
                if keyword in frequency_word:
                    tmp_total += frequency_word[keyword] * self.__keywords_weigth[class_id][keyword]

            similarity_list[class_id] = tmp_total     

        sorted_similarity = sorted(similarity_list.items(), key=lambda x:x[1], reverse=True)

        return sorted_similarity[0][0]    

    def __classify_document_euclidian(self, text_document):
        frequency_word = self.__frequency_word(text_document)
        similarity_list = dict()

        for class_id in self.__keywords_weigth:
            tmp_total = 0
            for keyword in self.__keywords_weigth[class_id]:
                value = frequency_word[keyword] if keyword in frequency_word else 0.0
                tmp_total +=  pow(value - self.__keywords_weigth[class_id][keyword], 2) 

            for word in frequency_word.keys():
                if not word in self.__keywords_weigth[class_id]:
                    tmp_total +=  pow(frequency_word[word] - 0.0, 2) 
            similarity_list[class_id] = sqrt(tmp_total)     

        sorted_similarity = sorted(similarity_list.items(), key=lambda x:x[1])
        return sorted_similarity[0][0]

    def __frequency_word(self, text_document):
        word_list = utils.get_words(text_document)
        frequency_word = dict()
        for word in word_list:
            if word in frequency_word:
                frequency_word[word] += 1
            else:
                frequency_word[word] = 1
        return frequency_word

    def get_macroF(self):
        acum_recall = 0
        acum_precision = 0
        classes = len(self.__classes)
        for id_class in self.__classes:
            acum_recall += self.__tp[id_class] / (self.__tp[id_class] + self.__fn[id_class])
            acum_precision += self.__tp[id_class] / (self.__tp[id_class] + self.__fp[id_class]) #aqui  KeyError: 'C22' 'C03'

        recall = (1 / classes) * acum_recall
        presicion = (1 / classes) * acum_precision
        medidaF = (2 * recall * presicion) / (recall + presicion)
        print("macro medidaF", medidaF)

    def get_microF(self):
        print("tp", self.__tp)
        print("fn", self.__fn)
        print("fp", self.__fp)
        numerador = 0
        den_recall = 0
        den_precision = 0
        tr = 0
        tp = 0
        tm = 0
        self.__classes = sorted(self.__classes)
        for id_class in self.__classes:
            numerador = self.__tp[id_class]
            den_recall = self.__tp[id_class] + self.__fn[id_class]
            den_precision = self.__tp[id_class] + self.__fp[id_class]         
            #print(id_class)
            recall = numerador / den_recall
            presicion = numerador / den_precision
            try:
                medidaF = (2 * recall * presicion) / (recall + presicion)
                print("%s  %.2f & %.2f & %.2f \\\\" % (id_class, presicion, recall,  medidaF))
            except:
                print(id_class, "zero")
            tr += recall
            tp += presicion
            tm += medidaF
        print(tp / 5.0, tr / 5.0, tm / 5.0)

    def print_matrix(self):
        for key, value in self.__confusion_matrix.items():
            print(key, value)

    def get_accuracy(self):
        self.__classes = sorted(self.__classes)
        for id_class in self.__classes:
            accuracy = self.__tp[id_class] / self.__elements [id_class]
            print("%s  %.2f\\\\" % (id_class, accuracy))