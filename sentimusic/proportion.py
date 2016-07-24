# -*- coding: utf-8 -*-

import operator

# ---------------------------------------------------------------------------
# Função get_proportion(): Função para detectar as proporções de sentimentos
#                          nos grupos do KMeans e classificar cada grupo de 
#                          acordo com a maior proporção. Retorna um dicionário
#                          com a classificação de cada grupo.
# - array: Lista com o número do grupo (cluster) de cada musica
# - music_dict: Dicionario contendo as musicas e seus respectivos sentimentos
#               e posições na matriz svd        
# - music_list: Lista com as urls (id) das musicas ordenadas
# ---------------------------------------------------------------------------
def get_proportion(array, music_dict, music_list):
    # Cria um dicionário para contar quantas musicas estão em cada grupo
    count_dict = {
        0: 0,
        1: 0,
        2: 0
    }

    # Cria dicionários para determinar a proporção dos sentimentos em cada grupo
    zeros_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }
    ones_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }
    twos_sentiment_prop = {
        'pos': .0,
        'neg': .0,
        'neutral': .0
    }

    #Dicionário que será retornado com a classificação de cada grupo
    group_sentiment = {
        0: '',
        1: '',
        2: ''
    }

    # Para cada número no array, ele verifica a qual grupo pertence e 
    # verifica o sentimento da música daquela posição
    for i in range(0, len(array)):
        count_dict[array[i][0]] += 1
        if array[i][0] == 0:
            zeros_sentiment_prop[music_dict[music_list[i]]['sentiment']] += 1
        elif array[i][0] == 1:
            ones_sentiment_prop[music_dict[music_list[i]]['sentiment']] += 1
        else:
            twos_sentiment_prop[music_dict[music_list[i]]['sentiment']] += 1

    # No final, temos a quantidade de sentimentos por grupo

    # Verificamos o maior valor do dicionário e usamos a sua chave 
    # (o sentimento) para classificar cada grupo
    group_sentiment[0] = max(zeros_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]
    group_sentiment[1] = max(ones_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]
    group_sentiment[2] = max(twos_sentiment_prop.iteritems(), key=operator.itemgetter(1))[0]

    return group_sentiment


