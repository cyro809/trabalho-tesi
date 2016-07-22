# -*- coding: utf-8 -*-

import cv2
import numpy as np

from k_fold import build_k_fold
from distance_utils import get_minimum_distance_label
from proportion import get_proportion

class KMeans:
    labels = []
    centers = []
    centers_labels = []
    retValues = []
    final_matrix = []
    total_test_length = 0
    best_accuracy = 0
    best_accuracy_train = 0

    def __init__(self, music_list, svd_matrix, music_dict, iterations=100, window_size=15):
        self.matrix = svd_matrix
        self.music_dict = music_dict
        # Cria os folds do K Fold, separando em treinamento e teste
        self.kfold_trainings, self.kfold_tests = build_k_fold(music_list, window_size)

        # Criterio para o opencv K Means
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, iterations, 1.0)


    def execute_kfold_training(self):
        current_accuracy = 0.
        for i in range(0,len(self.kfold_trainings)):
            score = 0.
            accuracy = 0.
            train_matrix = [self.matrix[self.music_dict[x]['pos']] for x in self.kfold_trainings[i]]
            train_matrix = np.float32(train_matrix)

            test_matrix = [self.matrix[self.music_dict[x]['pos']] for x in self.kfold_tests[i]]
            test_matrix = np.float32(test_matrix)

            ret,label,center=cv2.kmeans(train_matrix,3,None, self.criteria,10,cv2.KMEANS_RANDOM_CENTERS)

            center_labels = get_proportion(label, self.music_dict, self.kfold_trainings[i])

            for j in range(0,len(test_matrix)):
                total_test_length = len(test_matrix)
                music_label = get_minimum_distance_label(center, test_matrix[j])
                if center_labels[music_label] == self.music_dict[self.kfold_tests[i][j]]['sentiment']:
                    score += 1

            accuracy = score/total_test_length
            print '**********************************************'
            print
            print
            print 'Execution ', i, '- Accuracy: ', accuracy
            print
            print
            print '**********************************************'

            # Verifica a pontuação do treinamento atual do K Means
            if accuracy > current_accuracy:
                self.final_matrix = train_matrix
                self.final_center = center
                self.best_accuracy = accuracy
                self.best_accuracy_train = i


            self.labels.append(label)
            self.centers.append(center)
            self.retValues.append(ret)


    def execute_test(self, test_matrix):
        pass