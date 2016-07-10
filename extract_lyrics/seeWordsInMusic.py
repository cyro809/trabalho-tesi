#Project Music____
#This program receive a lyric from a music and print:
#Red:   Nouns
#Green: Verbs
#Blue:  Adjectives

#Import:
import nltk
import json
from nltk import word_tokenize
from collections import defaultdict

#Funcions and Colors:
def red(name):
    return "\033[91m{}\033[00m".format(name)

def green(name):
    return "\033[92m{}\033[00m".format(name)
    
def blue(name):
    return "\033[94m{}\033[00m".format(name)

def startWith(string, firstLetter):
    if (string[0] == firstLetter):
        return True
    return False
    
#Main:    
with open('database.json') as data_file:    
    data = json.load(data_file)

print("")
inputFile = input("Entre com qual música você deseja imprimir: ")
print("")  
sentence = data[int(inputFile)]["lyrics"]

tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
tokens = word_tokenize(sentence)

freqDict = defaultdict(int)
for token in tokens:
    freqDict[token] += 1

print(freqDict)
print("")
print(len(freqDict))
