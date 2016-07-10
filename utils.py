#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import codecs
import fileinput

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