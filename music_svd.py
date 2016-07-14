import numpy as np
import fileinput
from utils import read_json, remove_special_characters
from sklearn.cluster import KMeans
from proportion import get_proportion


class MusicSVD:
    word_list = []
    word_list_length = 0
    word_dict = {}

    music_list = []
    music_list_length = 0
    music_dict = {}
    
    
    def build_initial_matrix(self, json_array):
        initial_matrix = np.zeros(shape=(self.music_list_length, self.word_list_length), dtype=int)    
        for music in json_array:
            music['lyrics'] = remove_special_characters(music['lyrics'].lower().encode('utf-8'))
            self.music_dict[music['url']]['sentiment'] = music['sentiment']
            for i in range(0,20):
                for music_word in music['lyrics'].split():
                    if self.word_list[i].lower().strip() == music_word:
                        initial_matrix[self.music_dict[music['url']]['pos']][self.word_dict[self.word_list[i]]] += 1

        return initial_matrix



    def get_word_list(self, filename):
        with open(filename, 'r') as fp:
            self.word_list = fp.readlines()
            self.word_list_length = len(self.word_list)
            for i in range(0,self.word_list_length):
                self.word_dict[self.word_list[i]] = i

    def get_music_list(self, filename):
        with open(filename, 'r') as fp:
            self.music_list = fp.readlines()
            self.music_list_length = len(self.music_list)
            for i in range(0,self.music_list_length):
                self.music_dict[self.music_list[i].strip()] = {'pos': i, 'sentiment': ''}

    def calculate_svd(self, matrix):
        P, D, Q = np.linalg.svd(matrix, full_matrices=False)
        X_a = np.dot(np.dot(P, np.diag(D)), Q)
        return X_a



music_svd = MusicSVD()
music_svd.get_word_list('extract_lyrics/wordVect.txt')
music_svd.get_music_list('teste.txt')
json_array = read_json('database.json')
initial_matrix = music_svd.build_initial_matrix(json_array)
# for i in range(0,20):
#     print '#########################################################'
#     print music_svd.word_list[i]
#     print '#########################################################'
#     print svd_matrix[i]
#     print '---------------------------------------------------------'

svd_matrix = music_svd.calculate_svd(initial_matrix)
kmeans = KMeans(n_clusters=3)
kmeans.fit(svd_matrix)
for i in range(0,200):
    print "Music: ", music_svd.music_list[i].strip()
    print "Label: ", kmeans.labels_[i]
    print "Sentiment: ", music_svd.music_dict[music_svd.music_list[i].strip()]['sentiment']
    print
get_proportion(kmeans.labels_, music_svd.music_dict, music_svd.music_list)
