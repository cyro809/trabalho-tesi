#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math


def calculate_distance(p,q, n):
    result = 0
    for i in range(0,n):
        result += (p[i] - q[i])**2

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