#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

# ---------------------------------------------------------------------------
# Função calculate_distance(): Calcula a distancia euclidiana entre dois pontos
# - vec1: Vetor 1
# - vec2: Vetor 2
# - num: Número de dimensões espaciais
# ---------------------------------------------------------------------------
def calculate_distance(p1,p2, num):
    result = 0
    for i in range(0,num):
        result += (p1[i] - p2[i])**2

    return math.sqrt(result)

# ---------------------------------------------------------------------------
# Função get_minimum_distance_label(): Calcula a menor distancia entre a
#                                      musica e os centroides retornando o 
#                                      grupo a qual ela pertence
# - centers: Centroides de cada grupo
# - music: Coordenadas da musica no espaço
# ---------------------------------------------------------------------------
def get_minimum_distance_label(centers, music):
    min_distance = 1000
    label = 0
    for i in range(0, len(centers)):
        distance = calculate_distance(music, centers[i], len(centers[i]))
        if distance < min_distance:
            min_distance = distance
            label = i

    return label