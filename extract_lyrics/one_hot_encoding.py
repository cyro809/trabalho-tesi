#Project:

#Import:
import re
import nltk
import json
import enchant
import operator
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk import word_tokenize
from collections import defaultdict
from nltk.stem.porter import PorterStemmer
import sys

#Functions:
def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)

#Variables:
d = enchant.Dict("en_US")                       #Words in English in enchant (python)
stop_words = set(stopwords.words('english'))    #Stopwords from nltk
porter_stemmer = PorterStemmer()                #Steammer  from nltk
nM = 100                                        #Number of musics:

#Open File from JSON
with open('database.json') as data_file:    
    data = json.load(data_file)

#FinalWords:
finalDict = {}

for i in range(0,200):
    #Print progress bar:
    sys.stdout.write("\rProgress: %d%%" % i)
    sys.stdout.flush()
    
    #Read sentence:
    sentence = data[i]["lyrics"]

    #Tokenizer:
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    tokens = word_tokenize(sentence)
    #print(tokens)
    
    #Delete bad words:
    tokens[:] = [value.lower() for value in tokens]                      #Word lower case
    tokens[:] = (value for value in tokens if not value in stop_words)   #Remove stopwords
    tokens[:] = (value for value in tokens if d.check(value))            #Word in dict
    tokens[:] = (porter_stemmer.stem(value) for value in tokens)         #Stem all words    
    tokens[:] = (value for value in tokens if len(value) > 3)            #Word Size > 3      
    
    #CreateDict:
    freqDict = defaultdict(int)
    for token in tokens:
        freqDict[token] += 1
    
    #Join with final Dict:
    finalDict = dictSum(finalDict, freqDict)
    
#for key, value in finalDict.items():
#        if value <= 5:
#            del finalDict[key]
 
finalDict = {key:value for key, value in finalDict.items() if value >= 2}
            
sys.stdout.write("\rProgress: %d%%" % 100)
    
print("")
print("")
print("-----------------------------------")
print("Lenght of dict: " + str(len(finalDict)))
print("Musics " + str(nM))
print("-----------------------------------")
print("")

wordVect = open("wordVect", "w")
sorted_finalDict = sorted(finalDict.items(), key=operator.itemgetter(1), reverse=True)
for item in sorted_finalDict:
    wordVect.write(item[0] + " - " + str(item[1]) + "\n" )
