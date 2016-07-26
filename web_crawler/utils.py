#! /usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import fileinput
import json

# ---------------------------------------------------------------------------
# Função write_json(): Escreve o arquivo json com a lista de dicionários
#                      com as músicas
# - filename: Nome do arquivo que será escrito
# - lyrics_array: Lista de dicionários com as informações da músicas
# ---------------------------------------------------------------------------
def write_json(filename, lyrics_array):
    with codecs.open(filename, 'w', encoding='utf-8') as fp:
        json.dump(lyrics_array, fp, ensure_ascii=False, indent=4, separators=(',', ': '))


# ---------------------------------------------------------------------------
# Função read_json(): Lê o arquivo json com as informações das músicas
# - filename: Nome do arquivo json que será lido
# ---------------------------------------------------------------------------
def read_json(filename):
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as fp:
            content = json.load(fp)
            return content
    except IOError:
        return []

# ---------------------------------------------------------------------------
# Função read_urls_file(): Lê o arquivo com as urls e retorna uma lista de urls
# ---------------------------------------------------------------------------
def read_urls_file(filename):
    urls_array = []
    for url in fileinput.input(filename):
        url = url.strip()
        urls_array.append(url)
    return urls_array

# ---------------------------------------------------------------------------
# Função read_urls_input(): Le as urls através do terminal ou linha de comando
# ---------------------------------------------------------------------------
def read_urls_input():
    urls_array = []
    urls = raw_input('Insert the lyrics url separated by ",": \n')
    urls_array = urls.split(',')
    return urls_array
