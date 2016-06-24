#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from musics import Musics
from helpers import read_json, write_json

lyrics_json = []


class VagalumeSpider(Spider):
    name = "vagalume"
    allowed_domains = ["vagalume.com.br"]
    start_urls = Musics.URLS


    # def __init__(self, artists=None, *args, **kwargs):
    #     super(VagalumeSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ["http://www.vagalume.com.br/%s" % artist for artist in artists]

    def parse(self, response):
        sel = Selector(response)
        artist_path = sel.xpath('//*[@id="header"]/p[1]/a/text()')[0]
        artist = artist_path.extract()

        title_path = sel.xpath('//*[@id="header"]/h1/text()')[0]
        title = title_path.extract()
        title = title.strip()

        lyrics_path = sel.xpath('//*[@id="lyr_original"]/div')[0]
        lyrics = lyrics_path.extract()

        lyrics = lyrics.replace("<br>", "\n")
        lyrics = re.sub('<.*?>', '', lyrics)
        item = {
            'artist': artist.encode('utf-8'),
            'title': title.encode('utf-8'),
            'lyrics': lyrics.encode('utf-8'),
            'theme': ''.encode('utf-8'),
            'sentiment': ''.encode('utf-8'),

        }
        lyrics_json.append(item)
        return lyrics


if __name__ == "__main__":
    lyrics_json = read_json('result.json')

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(VagalumeSpider)
    process.start()
    write_json('result.json', lyrics_json)


