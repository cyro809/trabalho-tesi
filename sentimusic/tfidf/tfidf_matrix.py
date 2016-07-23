# -*- coding: utf-8 -*-

import tfidf_helpers as f
import json
import numpy as np

def generate_matrix(filename):
    #Open corpus (Open File from JSON):
    with open("../%s"%filename) as data_file:    
        data = json.load(data_file)

    #Create a list of words (Our vocabulary) and prepare the documents:
    vocabulary = f.build_lexiconAndDocuments(data)
    
    
    music_dict = {}
    music_list = []
    #Make doc_tf_vector in docList:
    doc_term_matrix = []
    for i in range(0,len(data)):
        doc_vector = [f.freq(word, i) for word in vocabulary]
        #tf_vector_string = ", ".join(format(freq, "d") for freq in tf_vector)
        doc_term_matrix.append(doc_vector)

        # Lista de Musicas (URLS) e dicionario com a posição e o sentimento de cada musica
        music_list.append(data[i]['url'])
        music_dict[data[i]['url']] = {'pos': i, 'sentiment': data[i]['sentiment']}
        
    #Transform in numpy matrix:
    doc_term_matrix = np.matrix(doc_term_matrix)

    return (doc_term_matrix, vocabulary, music_list, music_dict)
#----------------------------------------------

#Normalize vector:
#doc_term_matrix_normalized = f.normalizeMatrix(doc_term_matrix)

#print(doc_term_matrix_normalized)
