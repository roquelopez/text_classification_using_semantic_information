# -*- coding: utf-8 -*-
'''
Created on 22/07/2013

@author: roque
'''

import string
from nltk import word_tokenize
from nltk.corpus import stopwords

def get_words(text):
    tokens = word_tokenize(text.lower())
    stop_words_list = stopwords.words('english')
    t = [x[:-1] if x.endswith('.') else x for x in tokens if x not in stop_words_list if x not in string.punctuation]
    return t
    
def semantic_weights(file_path):
    my_list = dict()
    file = open(file_path, 'r', encoding='utf-8')
    while True:
        line = file.readline()
        if not line: break
        tmp_list = line.split(' ')
        my_list[tmp_list[1]+'_'+tmp_list[2]] = float(tmp_list[3].strip())
    file.close()
    return my_list
       
def read_file(file_path):
    my_file = open(file_path,"r", encoding='utf-8')
    text = my_file.read()
    my_file.close()
    return text