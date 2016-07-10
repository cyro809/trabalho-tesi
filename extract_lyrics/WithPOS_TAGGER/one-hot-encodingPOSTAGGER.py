#Project:

#Import:
import re
import nltk
import json
from nltk import word_tokenize
import time
import sys

#Functions:
def startWith(string, firstLetter):
    if (string[0] == firstLetter):
        return True
    return False

#Open File from JSON
with open('database.json') as data_file:    
    data = json.load(data_file)

#FinalWords:
finalAdjectives = []
finalVerbs = []
finalNouns = []
finalAll = []

for i in range(0,100):
    #Print progress bar:
    #time.sleep(1)
    sys.stdout.write("\rProgress: %d%%" % i)
    sys.stdout.flush()
    
    #Read sentence:
    sentence = data[i]["lyrics"]
    
    #Preprocess music:
    sentencePreprocessed = sentence.replace(".", " .") #Não funciona
    sentencePreprocessed = sentence.replace("\n", ". ")

    #Tokenizer:
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    tokens = word_tokenize(sentencePreprocessed)

    #Error from preprocess:
    tokens[:] = (value for value in tokens if value != ".")

    #Pos_Tag:
    post_tag = nltk.pos_tag(tokens)

    #FinalWords:
    verbs = []
    names = []
    adjectives = []
    for i in range(len(post_tag)):
        if (startWith(post_tag[i][1], "J")):
            adjectives.append(post_tag[i][0].lower())
        if (startWith(post_tag[i][1], "V")):
            verbs.append(post_tag[i][0].lower())
        if (startWith(post_tag[i][1], "N")):
            names.append(post_tag[i][0].lower())
    
    #Organize in a list:
    fv = list(set(verbs))
    fn = list(set(names))
    fa = list(set(adjectives))
    
    finalVerbs = finalVerbs + list(set(fv) - set(finalVerbs))
    finalNouns = finalNouns + list(set(fn) - set(finalNouns))
    finalAdjectives = finalAdjectives + list(set(fa) - set(finalAdjectives))
    finalAll = finalAll + finalVerbs + finalNouns + finalAdjectives
    finalAll = list(set(finalAll))

#Print Final Result:
vecWordFile = open("vecWord.txt", "w")
for i, items in enumerate(sorted(finalAll)):
    if items in finalVerbs:
        vecWordFile.write(items + " VERB" + "\n")
    if items in finalNouns:
        vecWordFile.write(items + " NOUN" + "\n")
    if items in finalAdjectives:
        vecWordFile.write(items + " ADJECTIVE" + "\n")

sys.stdout.write("\rProgress: %d%%" % 100)
#print("")
#print("Final Verbs: ")
#print("")
#print("")
#print(finalVerbs)
#print("")
#print("")
#print("Final Nouns: ")
#print("")
#print("")
#print(finalNouns)
#print("")
#print("")
#print("Final Adjectives")
#print("")
#print("")
#print(finalAdjectives)
#print("")
#print("")
#print("Final all words:")
#print(finalAll)
#print("")
#print("")
print("")
print("")
print("-----------------------------------")
print("Lenght of verbs: " + str(len(finalVerbs)))
print("Lenght of nouns: " + str(len(finalNouns)))
print("Lenght of adjectives: " + str(len(finalAdjectives)))
print("-----------------------------------")
print("")
