#Project Music____
#This program receive a lyric from a music and print:
#Red:   Nouns
#Green: Verbs
#Blue:  Adjectives

#Import:
import re
import nltk
import json
from nltk import word_tokenize
import time
import sys

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

sentencePreprocessed = sentence.replace(".", " .")
sentencePreprocessed = sentence.replace("\n", ". ")

tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
tokens = word_tokenize(sentencePreprocessed)
post_tag = nltk.pos_tag(tokens)

print("")
print(sentence)
print("")
print("-----------------------------")
print("")
newSentence = "|"
for i in range(len(post_tag)):
    if post_tag[i][0] == ".":
        print(newSentence)
        newSentence = "|"
    else:
        if (startWith(post_tag[i][1], "N")):
            newSentence = newSentence + red(post_tag[i][0]) + "| "
        elif (startWith(post_tag[i][1], "V")):
            newSentence = newSentence + green(post_tag[i][0]) + "| "
        elif (startWith(post_tag[i][1], "J")):
            newSentence = newSentence + blue(post_tag[i][0]) + "| "           
        else: 
            newSentence = newSentence + post_tag[i][0] + "| "
