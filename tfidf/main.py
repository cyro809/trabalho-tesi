import tfidfFunctions as f
import json
import numpy as np

def generateTFIDF_matrix():
    #Open corpus (Open File from JSON):
    with open("database.json") as data_file:    
        data = json.load(data_file)

    #Create a list of words (Our vocabulary) and prepare the documents:
    vocabulary = f.build_lexiconAndDocuments(data)

    #Make doc_tf_vector in docList:
    doc_term_matrix = []
    for i in range(0,100):
        doc_vector = [f.freq(word, i) for word in vocabulary]
        #tf_vector_string = ", ".join(format(freq, "d") for freq in tf_vector)
        doc_term_matrix.append(doc_vector)
        
    #Transform in numpy matrix:
    doc_term_matrix = np.matrix(doc_term_matrix)
    print(type(doc_term_matrix))
    return doc_term_matrix
#----------------------------------------------

#Normalize vector:
#doc_term_matrix_normalized = f.normalizeMatrix(doc_term_matrix)

#print(doc_term_matrix_normalized)
