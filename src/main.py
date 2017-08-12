# -*- coding: utf-8 -*-
'''
Created on 17/07/2013

@author: roque
'''

from keyword_extraction import KeywordExtraction
from classification import Classifier
from keyword_ranking import KeywordRanking
from rocchio import Rocchio

def print_rank(class_list):
    for id_class, keywords  in class_list.items():
        sorted_list = sorted(keywords.items(), key=lambda x:x[1], reverse=True)
        print(id_class, sorted_list[:10])

if __name__ == '__main__':
    training_folder_path = "../resource/ohsumed/training/"
    test_folder_path = "../resource/ohsumed/test/"
    #r = Rocchio()
    #r.train(training_folder_path)
    #r.test(test_folder_path)

    print("EXTRACTING") 
    ke = KeywordExtraction()
    ke.create_class(training_folder_path)
    keywords_by_class = ke.extract_keywords(3, training_folder_path)
    print("RANKING") 
    kr = KeywordRanking()
    keywords_by_class = kr.rank_keywords(training_folder_path, keywords_by_class)
    print_rank(keywords_by_class)
    print("CLASSIFYING")            
    c = Classifier(keywords_by_class)
    c.classify_all(test_folder_path)
    c.get_microF()