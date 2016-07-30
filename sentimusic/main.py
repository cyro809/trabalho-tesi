# -*- coding: utf-8 -*-

import numpy as np
from tfidf.tfidf_matrix import generate_matrix
from music_svd import calculate_svd
from kmeans import KMeans

EXECUTE_BEST_KFOLD = 1
EXECUTE_ALL_KFOLDS = 2

print "Database size: 435"

run_type = raw_input('Select the test execution type: \n1 - Execute Best K-Fold \n2- Execute All K-Folds \n')
run_type = int(run_type)

if run_type != EXECUTE_BEST_KFOLD or run_type != EXECUTE_ALL_KFOLDS:
    return 'Not a valid execution type! Ending program.'
train_length = raw_input('Training Set Length: \n')
print
K = raw_input('SVD K cut: \n')
print
window_size = raw_input('KFold window size: \n')
print
train_length = int(train_length)
K = int(K)
window_size = int(window_size)

filename = 'final_database.json'
initial_matrix, vocabulary, music_list, music_dict = generate_matrix(filename)

# Calcula o SVD e retorna os vetor (de tamanho k=4) espaciais das musicas
svd_matrix = calculate_svd(initial_matrix, K)

# Separa o conjunto inicial em treinamento e teste (Primeiro a matriz SVD e depois a lista de musicas)
train_matrix = [ svd_matrix[i] for i in range(0,train_length)]
final_test_matrix = [ svd_matrix[i] for i in range(train_length,len(svd_matrix))]

train_music_list = [ music_list[i] for i in range(0,train_length)]
final_test_music_list = [ music_list[i] for i in range(train_length,len(music_list))]

# Executa o KMeans com com conjunto de treinamento para saber qual é o melhor
kmeans = KMeans(train_music_list, window_size=window_size, iterations=1000)

if run_type == EXECUTE_BEST_KFOLD:
    kmeans.execute_kfold_training(train_matrix, music_dict)

    # Depois de escolhido o melhor conjunto de treinamento, executa o teste final para as musicas restantes
    kmeans.execute_best_test(final_test_matrix, music_dict, final_test_music_list)
else:
    # Executa o KMeans com todos os K-Folds de treinamento
    kmeans.execute_all_k_fold_tests(svd_matrix, final_test_matrix, music_dict)