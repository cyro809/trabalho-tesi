#Project:

#Import:
import re
import nltk
import json
from nltk import word_tokenize
from collections import defaultdict
import sys

#Functions:
def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)

#Open File from JSON
with open('database.json') as data_file:    
    data = json.load(data_file)

#Number of musics:
nM = 100

#FinalWords:
finalDict = {}

for i in range(0,nM):
    #Print progress bar:
    sys.stdout.write("\rProgress: %d%%" % i)
    sys.stdout.flush()
    
    #Read sentence:
    sentence = data[i]["lyrics"]

    #Tokenizer:
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    tokens = word_tokenize(sentence)

    #Delete bad words:
    tokens[:] = (value.lower() for value in tokens)
    tokens[:] = (value for value in tokens if len(value) > 1)
    
    
    #CreateDict:
    freqDict = defaultdict(int)
    for token in tokens:
        freqDict[token] += 1
    
    #Join with final Dict:
    finalDict = dictSum(finalDict, freqDict)
    
sys.stdout.write("\rProgress: %d%%" % 100)

print("")
print("")
print("-----------------------------------")
print("Lenght of dict: " + str(len(finalDict)))
print("Musics " + str(nM))
print("-----------------------------------")
print("")

wordVect = open("wordVect", "w")
for item in finalDict.items():
    wordVect.write(item[0] + "\n")
