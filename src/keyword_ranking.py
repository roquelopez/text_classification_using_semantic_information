# -*- coding: utf-8 -*-
'''
Created on 22/07/2013

@author: roque
'''

import os
from text_graph import TextGraph
from semantic_rank import SemanticRank

class KeywordRanking(object):

    def rank_keywords(self, folder_path, keywords_by_class):
        tmp_dict = dict()

        for id_class in keywords_by_class:
            tg = TextGraph(keywords_by_class[id_class])
            tg.create_text_graph(os.path.join(folder_path, id_class))
            sr = SemanticRank(tg.get_edges(), tg.get_vertices())
            tmp_dict[id_class] = sr.get_ranking_list()
        return tmp_dict