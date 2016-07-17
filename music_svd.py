import cv2
import numpy as np
import fileinput
from utils import read_json, remove_special_characters
from proportion import get_proportion

KMEANS_ITERATIONS = 100

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
                self.word_list.append(line.strip())
            self.word_list_length = len(self.word_list)
            for i in range(0,self.word_list_length):
                self.word_dict[self.word_list[i]] = i

    def get_music_list(self, filename):
        with open(filename, 'r') as fp:
            self.music_list = fp.readlines()
            self.music_list_length = len(self.music_list)
            for i in range(0,self.music_list_length):
                self.music_dict[self.music_list[i].strip()] = {'pos': i, 'sentiment': ''}

    def calculate_svd(self, matrix, k):
        print 'calculate_svd'
        U, sigma, V = np.linalg.svd(matrix, full_matrices=False)
        music_vectors = np.dot(np.diag(sigma), V[:,:k])
        Z = np.float32(music_vectors)
        print Z
        return Z



music_svd = MusicSVD()
music_svd.get_word_list('wordVect.txt')
music_svd.get_music_list('teste_min.txt')
json_array = read_json('database_min.json')
initial_matrix = music_svd.build_initial_matrix(json_array)
# for i in range(0,20):
#     print '#########################################################'
#     print music_svd.word_list[i]
#     print '#########################################################'
#     print svd_matrix[i]
#     print '---------------------------------------------------------'

svd_matrix = music_svd.calculate_svd(initial_matrix, 3)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, KMEANS_ITERATIONS, 1.0)
ret,label,center=cv2.kmeans(svd_matrix,3,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
print label