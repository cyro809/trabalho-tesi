from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

porter_stemmer = PorterStemmer()
snowball_stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()

while (True):
    print("")
    inputWord = input("Palavra: ")
    print("Porter: " + porter_stemmer.stem(inputWord))
    print("SnowBall: " + snowball_stemmer.stem(inputWord))
    print("WordnetLemma: " + wordnet_lemmatizer.lemmatize(inputWord))
