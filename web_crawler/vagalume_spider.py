#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from utils import read_json, write_json

# ---------------------------------------------------------------------------
# Classe VagalumeSpider: Spider usada para Crawl do site Vagalume.com.br
# ---------------------------------------------------------------------------
class VagalumeSpider(Spider):
    name = "vagalume"

    # Define os dominios permitidos a acesso
    allowed_domains = ["vagalume.com.br"]
    lyrics_array = []


    def __init__(self, *args, **kwargs):
        super(VagalumeSpider, self).__init__(*args, **kwargs)
        # Passa as urls para o crawl como chave no dicionário kwargs
        self.start_urls = kwargs.get('urls')

    # ---------------------------------------------------------------------------
    # Método parse(): Faz parse da resposta do crawl
    # - response: Resposta obtida no crawl
    # ---------------------------------------------------------------------------
    def parse(self, response):
        # Obtem os seletores (classes html e css da resposta)
        sel = Selector(response)

        # Obtem o nome do artista através do seletor xpath
        artist_path = sel.xpath('//*[@id="header"]/p[1]/a/text()')[0]
        artist = artist_path.extract()

        # Obtem o nome da música através do seletor xpath
        title_path = sel.xpath('//*[@id="header"]/h1/text()')[0]
        title = title_path.extract()
        title = title.strip()

        # Obtem letra músical através do seletor xpath
        lyrics_path = sel.xpath('//*[@id="lyr_original"]/div')[0]
        lyrics = lyrics_path.extract()

        # Trata as tags html presentes. Substitui tags <br> por \n
        lyrics = lyrics.replace("<br>", "\n")
        lyrics = re.sub('<.*?>', '', lyrics)
        lyrics = lyrics.strip()

        # Guarda os dados parseados num dicionário
        item = {
            'artist': artist,
            'title': title,
            'lyrics': lyrics,
            'theme': '',
            'sentiment': '',
            'url': response.url
        }

        #Salva numa lista de dicionários cada música parseada
        self.lyrics_array.append(item)
        return lyrics