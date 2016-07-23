import numpy as np
from utils import remove_special_characters

def build_word_count_matrix(json_array, music_dict, music_list, word_list):
    print 'build_initial_matrix'
    initial_matrix = np.zeros(shape=(music_list_length, word_list_length), dtype=int)    
    for music in json_array:
        music['lyrics'] = remove_special_characters(music['lyrics'].lower().encode('utf-8'))
        music_dict[music['url']]['sentiment'] = music['sentiment']
        for i in range(0,len(word_list)):
            for music_word in music['lyrics'].split():
                if word_list[i].lower().strip() == music_word:
                    initial_matrix[music_dict[music['url']]['pos']][word_dict[word_list[i]]] += 1

    return initial_matrix