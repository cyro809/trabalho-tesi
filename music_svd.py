import cv2
import numpy as np
import fileinput
from utils import read_json, remove_special_characters, get_minimum_distance_label
from proportion import get_proportion
from k_fold import build_k_fold

KMEANS_ITERATIONS = 100
K_FOLD_WINDOW_SIZE = 15

class MusicSVD:
    word_list = []
    word_list_length = 0
    word_dict = {}

    music_list = []
    music_list_length = 0
    music_dict = {}
    
    
    def build_initial_matrix(self, json_array):
        print 'build_initial_matrix'
        initial_matrix = np.zeros(shape=(self.music_list_length, self.word_list_length), dtype=int)    
        for music in json_array:
            music['lyrics'] = remove_special_characters(music['lyrics'].lower().encode('utf-8'))
            self.music_dict[music['url']]['sentiment'] = music['sentiment']
            for i in range(0,len(self.word_list)):
                for music_word in music['lyrics'].split():
                    if self.word_list[i].lower().strip() == music_word:
                        initial_matrix[self.music_dict[music['url']]['pos']][self.word_dict[self.word_list[i]]] += 1

        return initial_matrix



    def get_word_list(self, filename):
        with open(filename, 'r') as fp:
            for line in fp:
                if len(line) > 4:
                    self.word_list.append(line.strip())
            self.word_list_length = len(self.word_list)
            for i in range(0,self.word_list_length):
                self.word_dict[self.word_list[i]] = i

    def get_music_list(self, filename):
        with open(filename, 'r') as fp:
            self.music_list = fp.readlines()
            self.music_list_length = len(self.music_list)
            for i in range(0,self.music_list_length):
                self.music_list[i] = self.music_list[i].strip()
                self.music_dict[self.music_list[i]] = {'pos': i, 'sentiment': ''}

    def calculate_svd(self, matrix, k):
        print 'calculate_svd'
        U, sigma, V = np.linalg.svd(matrix, full_matrices=False)
        music_vectors = np.dot(np.diag(sigma), V[:,:k])
        return music_vectors



music_svd = MusicSVD()
music_svd.get_word_list('wordVect.txt')
music_svd.get_music_list('teste_min.txt')

json_array = read_json('database_min.json')
initial_matrix = music_svd.build_initial_matrix(json_array)
svd_matrix = music_svd.calculate_svd(initial_matrix, 4)

kfold_trainings, kfold_tests = build_k_fold(music_svd.music_list, K_FOLD_WINDOW_SIZE)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, KMEANS_ITERATIONS, 1.0)
labels = []
centers = []
retValues = []

for i in range(0,len(kfold_trainings)):
    score = 0
    train_matrix = [svd_matrix[music_svd.music_dict[x]['pos']] for x in kfold_trainings[i]]
    train_matrix = np.float32(train_matrix)

    test_matrix = [svd_matrix[music_svd.music_dict[x]['pos']] for x in kfold_tests[i]]
    test_matrix = np.float32(test_matrix)

    ret,label,center=cv2.kmeans(train_matrix,3,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    center_labels = get_proportion(label, music_svd.music_dict, kfold_trainings[i])

    for j in range(0,len(test_matrix)):
        music_label = get_minimum_distance_label(center, test_matrix[j])
        if center_labels[music_label] == music_svd.music_dict[kfold_tests[i][j]]['sentiment']:
            score += 1

    print '**********************************************'
    print
    print
    print 'Execution ', i, '- Score: ', score
    print
    print
    print '**********************************************'
        
    labels.append(label)
    centers.append(center)
    retValues.append(ret)

