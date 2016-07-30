#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pycurl
import json

from urllib import urlencode

from scrapy.crawler import CrawlerProcess
from utils import read_json, write_json, read_urls_file, read_urls_input
from vagalume_spider import VagalumeSpider
from classifier import ClassifierResponse
from music_count import sentiment_count

from random import shuffle

# ---------------------------------------------------------------------------
# Função crawl_lyrics(): Faz o crawl de urls das letras músicais do site Vagalume.com.br e
#                        retorna uma lista de dicionários contendo o nome do
#                        artista, o titulo da música e a letra da música
# - urls_array: Lista de urls das letras músicais
# ---------------------------------------------------------------------------
def crawl_lyrics(urls_array):
    # Cria uma instancia de VagalumeSpider passando como parametro a lista de urls
    v_spider = VagalumeSpider(urls=urls_array)

    # Cria uma instancia de CrawlerProcess com USER_AGENT = Mozilla/4.0 que
    # será usado para fazer o crawl da música
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    # Faz o crawl com a instancia do VagalumeSpider
    process.crawl(v_spider, urls=urls_array)
    process.start()

    # Retorna a lista de dicionários com os dados das músicas.
    return v_spider.lyrics_array


# ---------------------------------------------------------------------------
# Função classify_lyrics(): Classifica os sentimentos de cada letra musical 
#                           em uma lista de músicas 
# - lyrics_array: Uma lista de dicionários com as informações da musica
# ---------------------------------------------------------------------------
def classify_lyrics(lyrics_array):
    # Criamos uma lista vazia que será preenchida com todas as músicas após
    # serem classificadas
    classified_array = []
    sys.stderr.write("Classifying Lyrics...\n")

    # Cria uma instancia do pycurl para fazer a requisição na API do site 
    # que classifica a letra
    c = pycurl.Curl()

    # Para cada música, fazemos a requisição com passando a letra como parametro do Curl
    for music in lyrics_array:
        t = ClassifierResponse()
        lyric = {
            'text': music['lyrics'].encode('utf-8')
        }

        # Adicionamos o parametro no Curl
        postfields = urlencode(lyric)

        # Adicionamos as opções do Curl (Site, tipo de requesição e a resposta da requisição)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(c.URL, 'http://text-processing.com/api/sentiment/')
        c.setopt(c.WRITEFUNCTION, t.body_callback)

        # Executamos o curl
        c.perform()

        # Recuperamos a resposta, que vem no formato de json e gravamos na
        # dicionário correspondente na chave sentiment
        result_dict = json.loads(t.contents)
        music['sentiment'] = result_dict['label']

        # Adicionamos a música classificada a lista de musicas classificadas
        classified_array.append(music)

    # Fechamos o Curl
    c.close()
    print "Done Classifying."
    print
    return classified_array


if __name__ == "__main__":

    # Nome do arquivo json que queremos fazer as operações
    json_filename = '../database_new.json'

    # Nome do arquivo com as urls novas que queremos adicionar no json
    input_filename = 'music_urls.txt'

    # Leitura do arquivo json. Caso não exista, retorna uma lista vazia
    database_array = read_json(json_filename)

    # Leitura do arquivo de urls
    urls_array = read_urls_file(input_filename) # Aqui colocamos a entrada desejada

    # Leitura das urls via input do usuário
    # urls_array = read_urls_input()

    # Chama a função para crawl das letras retornando uma lista de dicionários
    lyrics_array = crawl_lyrics(urls_array)
    
    # Adicionamos a nova lista ao final da lista de músicas que estavam
    # no banco de dados
    database_array.extend(classify_lyrics(lyrics_array))

    # Escrevemos no arquivo json
    write_json(json_filename, database_array)

    # Exibimos o total de musicas por sentimento no json
    sentiment_count(json_filename)

