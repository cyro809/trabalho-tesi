# -*- coding: utf-8 -*-

import cv2
import numpy as np
import fileinput
from utils import read_json, remove_special_characters

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

    def set_music_dict(self, music_list, music_sentiment_list):
            for i in range(0, len(music_list)):
                self.music_dict[music_list[i]] = {'pos': i, 'sentiment': music_sentiment_list[i]}

    def calculate_svd(self, matrix, k):
        print 'calculate_svd'
        U, sigma, V = np.linalg.svd(matrix, full_matrices=False)
        music_vectors = np.dot(np.diag(sigma), V[:,:k])
        return music_vectors
