import nltk
from nltk import word_tokenize

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

print("")
inputSentence = input("Diga qual problema você quer visualizar: ")

while(int(inputSentence) != 0):
    print("")
    
    #Change sentences:
    if(int(inputSentence) == 1):
        sentence = "He loves fast cars. Don’t drive so fast!"
    if(int(inputSentence) == 2):
        sentence = "Miss independent\nWon't you come and, spend a little time\nShe got her own thing\nThat's why I love her\nMiss independent\nOoh the way you shine\nMiss independent"   
    
    sentencePreprocessed = sentence.replace(".", " .")
    sentencePreprocessed = sentence.replace("\n", ". ")

    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    tokens = word_tokenize(sentencePreprocessed)

    post_tag = nltk.pos_tag(tokens)
    
    newSentence = ""
    for i in range(len(post_tag)):
        if post_tag[i][0] == ".":
            print(newSentence)
            newSentence = ""
        else:
            if (startWith(post_tag[i][1], "N")):
                newSentence = newSentence + red(post_tag[i][0]) + " "
            elif (startWith(post_tag[i][1], "V")):
                newSentence = newSentence + green(post_tag[i][0]) + " "
            elif (startWith(post_tag[i][1], "J")):
                newSentence = newSentence + blue(post_tag[i][0]) + " "           
            else: 
                newSentence = newSentence + post_tag[i][0] + " "
    print(newSentence)
    print("")
    inputSentence = input("Diga qual problema você quer visualizar: ")
    print("")
