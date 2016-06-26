#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pycurl
import json

from urllib import urlencode

from scrapy.crawler import CrawlerProcess
from utils import read_json, write_json, read_urls_file, read_urls_input
from vagalume_spider import VagalumeSpider
from test import Test


def crawl_lyrics(urls_array):
    v_spider = VagalumeSpider(urls=urls_array)
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(v_spider, urls=urls_array)
    process.start()
    return v_spider.lyrics_array

def classify_lyrics(lyrics_array):
    classified_array = []
    sys.stderr.write("Testing %s\n" % pycurl.version)
    c = pycurl.Curl()

    for music in lyrics_array:
        t = Test()
        lyric = {
            'text': music['lyrics'].encode('utf-8')
        }
        postfields = urlencode(lyric)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(c.URL, 'http://text-processing.com/api/sentiment/')
        c.setopt(c.WRITEFUNCTION, t.body_callback)
        c.perform()
        result_dict = json.loads(t.contents)
        music['sentiment'] = result_dict['label']
        classified_array.append(music)

    c.close()

    return classified_array


if __name__ == "__main__":
    json_filename = 'teste.json'
    input_filename = 'teste.txt'
    database_array = read_json(json_filename)
    urls_array = read_urls_file(input_filename) # Aqui colocamos a entrada desejada
    lyrics_array = crawl_lyrics(urls_array)
    
    database_array.extend(classify_lyrics(lyrics_array))
    write_json(json_filename, database_array)
