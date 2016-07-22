#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math


def calculate_distance(vec1,vec2, num):
    result = 0
    for i in range(0,num):
        result += (vec1[0][i] - vec2[i])**2

    return math.sqrt(result)

def get_minimum_distance_label(centers, music):
    min_distance = 1000
    label = 0
    for i in range(0, len(centers)):
        distance = calculate_distance(music, centers[i], len(centers[i]))
        if distance < min_distance:
            min_distance = distance
            label = i

    return label