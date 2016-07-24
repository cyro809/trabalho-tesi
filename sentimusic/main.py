import numpy as np
from tfidf.tfidf_matrix import generate_matrix
from music_svd import calculate_svd
from kmeans import KMeans



filename = 'database_min.json'
initial_matrix, vocabulary, music_list, music_dict = generate_matrix(filename)

train_length = 60

# Calcula o SVD e retorna os vetores (de tamanho k=4) espaciais das musicas
svd_matrix = calculate_svd(initial_matrix, 4)

# Separa o conjunto inicial em treinamento e teste (Primeiro a matriz SVD e depois a lista de musicas)
train_matrix = [ svd_matrix[i] for i in range(0,train_length)]
final_test_matrix = [ svd_matrix[i] for i in range(train_length,len(svd_matrix))]

train_music_list = [ music_list[i] for i in range(0,train_length)]
final_test_music_list = [ music_list[i] for i in range(train_length,len(music_list))]

# Executa o KMeans com com conjunto de treinamento para saber qual é o melhor
kmeans = KMeans(train_music_list)
kmeans.execute_kfold_training(train_matrix, music_dict)

# Depois de escolhido o melhor conjunto de treinamento, executa o teste final para as musicas restantes
kmeans.execute_best_test(final_test_matrix, music_dict, final_test_music_list)