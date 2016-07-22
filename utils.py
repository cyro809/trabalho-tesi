#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import codecs
import fileinput
import math
import json

def write_json(filename, lyrics_array):
    with codecs.open(filename, 'w', encoding='utf-8') as fp:
        json.dump(lyrics_array, fp, ensure_ascii=False, indent=4, separators=(',', ': '))


def read_json(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as fp:
            content = json.load(fp)
            return content
    except IOError:
        return []


def read_urls_file(filename):
    urls_array = []
    for url in fileinput.input(filename):
        url = url.strip()
        urls_array.append(url)
    print '###########################################################'
    print urls_array
    print '###########################################################'
    return urls_array

def read_urls_input():
    urls_array = []
    urls = raw_input('Insert the lyrics url separated by ",": \n')
    urls_array = urls.split(',')
    return urls_array

def remove_special_characters(text):
    text = text.strip()
    text = text.replace('\n\n', ' ')
    text = text.replace('\n', ' ')
    text = re.sub('[!,.()?]', ' ', text)
    return text

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