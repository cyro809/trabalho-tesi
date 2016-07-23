# -*- coding: utf-8 -*-

#Import:
import enchant
from nltk.corpus import stopwords
import sys
from nltk.stem.porter import PorterStemmer
import nltk
from nltk import word_tokenize
from collections import defaultdict
import numpy as np
import math
#---------------------------------------------------------------------------------------------#
#Utility functions:
def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)
    
#Utility variables:
d = enchant.Dict("en_US")                       #Words in English in enchant (python)
stop_words = set(stopwords.words('english'))    #Stopwords from nltk
porter_stemmer = PorterStemmer()                #Steammer  from nltk
tokenizer = nltk.data.load("tokenizers/punkt/english.pickle") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

                                       #Number of musics
list_of_documents = []                          #Cleaned documents (dict)
#---------------------------------------------------------------------------------------------#

def build_lexiconAndDocuments(data):
        
    finalWords = {}
    for i in range(0,len(data)):
        #Print progress bar:
        #sys.stdout.write("\rProgress: %d%%" % i)
        #sys.stdout.flush()
        
        #Read sentence:
        text = data[i]["lyrics"]

        #Return dictFreq
        freqDict = cleanText(text)
        list_of_documents.append(freqDict)
        
        #Join with final Dict:
        finalWords = dictSum(finalWords, freqDict)
     
    #finalWords = {key:value for key, value in finalWords.items() if value >= 2}   #clean words that appears only 2 times.
    
    return list(finalWords.keys())
    
def freq(term, i):
    return list_of_documents[i].get(term, 0)
    
def cleanText(text):
    
    #Tokenize:
    tokens = word_tokenize(text)
    #print(tokens)
        
    #Delete and transform bad words:
    tokens[:] = [value.lower() for value in tokens]                      #Word lower case
    tokens[:] = (value for value in tokens if not value in stop_words)   #Remove stopwords
    tokens[:] = (value for value in tokens if d.check(value))            #Word in dict
    tokens[:] = (porter_stemmer.stem(value) for value in tokens)         #Stem all words    
    tokens[:] = (value for value in tokens if len(value) > 3)            #Word Size > 3      
      
    #CreateDict:
    freqDict = defaultdict(int)
    for token in tokens:
        freqDict[token] += 1

    #Return dict or words:
    return freqDict
    
def normalizeVec(vec):
    denom = np.sum([el**2 for el in vec])
    return [(el / math.sqrt(denom)) for el in vec]
    
def normalizeMatrix(matrix):
    finalMatrix = []
    for vec in matrix:
        finalMatrix.append(normalizeVec(vec))
    return finalMatrix
