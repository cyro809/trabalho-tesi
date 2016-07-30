# -*- coding: utf-8 -*-

import cv2
import numpy as np

from k_fold import build_k_fold
from distance_utils import get_minimum_distance_label
from proportion import get_proportion

# ---------------------------------------------------------------------------
# Classe KMeans: Utilizada para executar o KMeans com validação cruazada KFold
# ---------------------------------------------------------------------------
class KMeans:
    labels = []
    centers = []
    centers_labels = []
    retValues = []
    final_matrix = []
    final_group_labels = {}
    total_test_length = 0
    best_accuracy = 0.
    best_accuracy_train = 0

    # ---------------------------------------------------------------------------
    # Construtor da classe KMeans
    # - music_list: Lista com as urls (id) das musicas ordenadas
    # - iterations: Quantas iterações o KMeans irá executar (default = 100)
    # - clusters: Quantidade de clusters (agrupados) que o KMeans irá agrupar as músicas
    # - window_size: Tamanho da janela para separação dos conjuntos no K Fold (default = 15)
    # - attempts: Número de vezes em que o algoritmo será executado com diferentes
    #             rotulamentos (default = 100)
    # ---------------------------------------------------------------------------
    def __init__(self, music_list, iterations=100, clusters=3, window_size=15, attempts=100):
        # Criterio para o opencv K Means
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, iterations, 1.0)
        self.num_clusters = clusters
        self.attempts = attempts
        
        # Cria os folds do K Fold, separando em treinamento e teste
        self.kfold_trainings, self.kfold_tests = build_k_fold(music_list, window_size)


    # ---------------------------------------------------------------------------
    # Método execute_kfold_training() - Executa os treinamentos separados pelo K Fold
    # - svd_matrix: Matriz SVD já calculada que será usada no aprendizado
    # - music_dict: Dicionario contendo as musicas e seus respectivos sentimentos
    #               e posições na matriz svd 
    # ---------------------------------------------------------------------------
    def execute_kfold_training(self, matrix, music_dict):
        current_accuracy = 0.

        for i in range(0,len(self.kfold_trainings)):
            
            # Constroi a matriz de treinamento obtendo o posicionamento das 
            # musicas conseguido do calculo do SVD
            train_matrix = [matrix[music_dict[x]['pos']] for x in self.kfold_trainings[i]]
            train_matrix = np.float32(train_matrix)

            # Constroi a matriz de treinamento obtendo o posicionamento das 
            # musicas conseguido do calculo do SVD
            test_matrix = [matrix[music_dict[x]['pos']] for x in self.kfold_tests[i]]
            test_matrix = np.float32(test_matrix)

            # Executa o Kmeans com os critérios definidos no construtor da classe KMeans
            ret,label,center=cv2.kmeans(train_matrix, self.num_clusters,None, self.criteria, self.attempts,cv2.KMEANS_RANDOM_CENTERS)

            # Obtem a proporção de cada grupo/centroide e o classifica de acordo
            # com a maioria
            group_labels = get_proportion(label, music_dict, self.kfold_trainings[i])

            # Executa o método execute_teste para testar o treinamento atual
            self.execute_test(music_dict, test_matrix, train_matrix, center, group_labels, i)

            # Guarda as informações dos K Means
            self.labels.append(label)
            self.centers.append(center)
            self.retValues.append(ret)
            self.centers_labels.append(group_labels)


    # ---------------------------------------------------------------------------
    # Método execute_test() - Executa a etapa de testes do aprendizado 
    #                         verificando a qual dos grupos as musicas pertencem
    # - music_dict: Dicionario contendo as musicas e seus respectivos sentimentos
    #               e posições na matriz svd
    # - test_matrix: matriz de teste que contem as posições de cada musica no SVD
    # - train_matrix: matriz usada para o treinamento do kmeans
    # - center: Centroides do treinamento atual
    # - group_labels: A classificação de cada centroide (pos, neg ou neutral)
    # - i: Execução atual do K Fold
    # ---------------------------------------------------------------------------
    def execute_test(self, music_dict, test_matrix, train_matrix, center, group_labels, i):
        score = 0.
        accuracy = 0.

        # Para cada musica, verificamos a distancia dela para os centroides
        for j in range(0,len(test_matrix)):
            total_test_length = len(test_matrix)
            music_label = get_minimum_distance_label(center, test_matrix[j])

            # Caso ela seja classificada de acordo com o sentimento da base dados,
            # acrescentamos +1 na pontuação do conjunto treinamento
            if group_labels[music_label] == music_dict[self.kfold_tests[i][j]]['sentiment']:
                score += 1

        
        # Calculamos a acuracia de acordo com a quantidade de musicas acertadas 
        # sobre o total de musicas testadas
        accuracy = score/total_test_length

        # Para saber a acuracia de cada teste, descomente as linhas abaixo
        # print '**********************************************'
        # print
        # print 'Execution ', i, '- Accuracy: ', accuracy
        # print
        # print '**********************************************'

        # Verifica a pontuação do treinamento atual do K Means e guarda a matriz
        # de treinamento, os centroids, a acuracia e o numero da execução
        if accuracy > self.best_accuracy:
            self.final_matrix = train_matrix
            self.final_center = center
            self.best_accuracy = accuracy
            self.best_accuracy_train = i
            self.final_group_labels = group_labels

    # ---------------------------------------------------------------------------
    # Método execute_best_test(): Executa a etapa de teste do aprendizado de
    #                             maquina com o melhor dos conjuntos do K Fold
    # - test_matrix: Matriz SVD que servirá para testes de aprendizado
    # - music_dict: Dicionario contendo as musicas e seus respectivos sentimentos
    #               e posições na matriz svd
    # - music_list: Lista das músicas de teste
    # ---------------------------------------------------------------------------
    def execute_best_test(self, test_matrix, music_dict, music_list):
        # Para cada musica, verificamos a distancia dela para os centroides
        accuracy = 0.
        score = 0.
        test_matrix = np.float32(test_matrix)
        for j in range(0,len(test_matrix)):
            total_test_length = len(test_matrix)
            music_label = get_minimum_distance_label(self.final_center, test_matrix[j])

            # Caso ela seja classificada de acordo com o sentimento da base dados,
            # acrescentamos +1 na pontuação do conjunto treinamento
            if self.final_group_labels[music_label] == music_dict[music_list[j]]['sentiment']:
                score += 1

        # Calculamos a acuracia de acordo com a quantidade de musicas acertadas 
        # sobre o total de musicas testadas
        accuracy = score/total_test_length
        
        #print '**********************************************'
        print '----------------------------------------------'
        #print
        print 'Test Execution ', '- Accuracy: ', accuracy
        #print
        print '----------------------------------------------'
        print '**********************************************'


    # ---------------------------------------------------------------------------
    # Método execute_all_k_fold_tests(): Executa a etapa de teste do aprendizado de
    #                             maquina com o melhor dos conjuntos do K Fold
    # - matrix: Matriz SVD usada como referencia para construir a matriz de treinamento
    # - test_matrix: Matriz SVD que servirá para testes de aprendizado
    # - music_dict: Dicionario contendo as musicas e seus respectivos sentimentos
    #               e posições na matriz svd
    # ---------------------------------------------------------------------------
    def execute_all_k_fold_tests(self, matrix, test_matrix, music_dict):
        current_accuracy = 0.

        for i in range(0,len(self.kfold_trainings)):
            
            # Constroi a matriz de treinamento obtendo o posicionamento das 
            # musicas conseguido do calculo do SVD
            train_matrix = [matrix[music_dict[x]['pos']] for x in self.kfold_trainings[i]]
            train_matrix = np.float32(train_matrix)

            test_matrix = np.float32(test_matrix)

            # Executa o Kmeans com os critérios definidos no construtor da classe KMeans
            ret,label,center=cv2.kmeans(train_matrix, self.num_clusters,None, self.criteria, self.attempts,cv2.KMEANS_RANDOM_CENTERS)

            # Obtem a proporção de cada grupo/centroide e o classifica de acordo
            # com a maioria
            group_labels = get_proportion(label, music_dict, self.kfold_trainings[i])

            # Executa o método execute_teste para testar o treinamento atual
            self.execute_test(music_dict, test_matrix, train_matrix, center, group_labels, i)

            # Guarda as informações dos K Means
            self.labels.append(label)
            self.centers.append(center)
            self.retValues.append(ret)
            self.centers_labels.append(group_labels)