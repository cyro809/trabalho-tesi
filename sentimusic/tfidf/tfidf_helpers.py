# -*- coding: utf-8 -*-

#Import
import sys
import enchant
from collections import defaultdict

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize

import numpy as np
import math

#---------------------------------------------------------------------------------------------#
#Utility functions

#Sum of two dicts
def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)
    
#Utility variables
d = enchant.Dict("en_US")                       #Words in English in enchant (python). It's a list of words in English.
stop_words = set(stopwords.words('english'))    #Stopwords from nltk.
porter_stemmer = PorterStemmer()                #Steammer(  from nltk.
tokenizer = nltk.data.load("tokenizers/punkt/english.pickle") #Tokenizer from nltk.

list_of_documents = []                          #Cleaned documents (dict)
#---------------------------------------------------------------------------------------------#

def build_lexiconAndDocuments(data):
    finalWords = {}
    for i in range(0,len(data)):
        #Read text
        text = data[i]["lyrics"]

        #Return dictionary of frequency of "clean" words    Ex: {w1 : f1, w2 : f2, w3 : f3, ...}
        freqDict = cleanText(text)
        list_of_documents.append(freqDict)
        
        #Join with final Dict that have all the words:
        finalWords = dictSum(finalWords, freqDict)
     
    #finalWords = {key:value for key, value in finalWords.items() if value >= 2}   #clean words that appears only 2 times.
    
    #Return a list of final words              Ex: [w1, w2, w3, w4, ...]
    return list(finalWords.keys())
    
#Remove "bad" words
def cleanText(text):
    
    #Tokenize     Ex: [w1, w2, w3, ...]
    tokens = word_tokenize(text) 
        
    #Delete and transform bad words
    tokens[:] = [value.lower() for value in tokens]                      #Word lower case
    tokens[:] = (value for value in tokens if not value in stop_words)   #Remove stopwords
    tokens[:] = (value for value in tokens if d.check(value))            #Word in dict
    tokens[:] = (porter_stemmer.stem(value) for value in tokens)         #Stem all words    
    tokens[:] = (value for value in tokens if len(value) > 3)            #Word Size > 3      
      
    #Create Dict and add 1 if a word appears. In the end, we will have a freqDict
    freqDict = defaultdict(int)
    for token in tokens:
        freqDict[token] += 1

    #Return freqDict    Ex: {w1 : f1, w2 : f2, w3 : f3, ...}
    return freqDict

def freq(term, i):
    return list_of_documents[i].get(term, 0)

#def normalizeVec(vec):
#    denom = np.sum([el**2 for el in vec])
#    return [(el / math.sqrt(denom)) for el in vec]
#    
#def normalizeMatrix(matrix):
#    finalMatrix = []
#    for vec in matrix:
#        finalMatrix.append(normalizeVec(vec))
#    return finalMatrix
    
#Get doc_term matrix, return tf_idf matrix:
def docTerm_to_tfIdfMatrix(doc_term_matrix_original):    
    doc_term_matrix = [doc_term_matrix_original[i][:] for i in range(len(doc_term_matrix_original))]    
    #TF(t) = (Number of times term t appears in a document)/(Total number of terms in the document)
    tf_matrix = docTerm_to_TF(doc_term_matrix)

    #IDF(t) = log(Total number of documents / Number of documents with term t in it) 
    idf_line = docTerm_to_IDF(doc_term_matrix)

    #Tf-idf = TF(t)*IDF(t)
    tfidf_matrix = multi_matrix(tf_matrix, idf_line)
    
    return tfidf_matrix
    
    
#------------------------------------------------    
def docTerm_to_TF(doc_term_matrix_original):
    doc_term_matrix = [doc_term_matrix_original[i][:] for i in range(len(doc_term_matrix_original))]
    number_lines = len(doc_term_matrix)
    number_columns = len(doc_term_matrix[0])
    totalSum = 0
    for i in range(number_lines):
        for j in range(number_columns):
            totalSum += doc_term_matrix[i][j]
        for j in range(number_columns):
            doc_term_matrix[i][j] = doc_term_matrix[i][j] / totalSum 
        totalSum = 0
    return doc_term_matrix
    
def docTerm_to_IDF(doc_term_matrix_original):
    doc_term_matrix = [doc_term_matrix_original[i][:] for i in range(len(doc_term_matrix_original))]
    number_lines = len(doc_term_matrix)
    number_columns = len(doc_term_matrix[0])
    totalSum = 0
    for j in range(number_columns):
        for i in range(number_lines):
            if(doc_term_matrix[i][j] != 0):
                totalSum += 1
        if totalSum:
            doc_term_matrix[0][j] = math.log10(number_lines/totalSum)
        else:
            doc_term_matrix[0][j] = 0
        totalSum = 0
    return doc_term_matrix[0]
    
def multi_matrix(tf_matrix, idf_vector):
    tf_matrix = np.array(tf_matrix)
    idf_vector = np.array(idf_vector)
    
    return tf_matrix*idf_vector
    
    



#Print progress bar:
        #sys.stdout.write("\rProgress: %d%%" % i)
        #sys.stdout.flush()
        

