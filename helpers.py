#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

import json

def write_json(filename, lyrics_dict):
    with codecs.open(filename, 'w', encoding='utf-8') as fp:
        json.dump(lyrics_dict, fp, ensure_ascii=False, indent=4, separators=(',', ': '))


def read_json(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as fp:
            content = json.load(fp)
            return content
    except IOError:
        return []
