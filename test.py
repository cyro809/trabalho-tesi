#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import pycurl
import json

from urllib import urlencode
from helpers import read_json, write_json

PY3 = sys.version_info[0] > 2


class Test:
    def __init__(self):
        self.contents = ''
        if PY3:
            self.contents = self.contents.encode('ascii')

    def body_callback(self, buf):
        self.contents = self.contents + buf


sys.stderr.write("Testing %s\n" % pycurl.version)

lyrics_dict = read_json('result.json')
classified_array = []

c = pycurl.Curl()

for music in lyrics_dict:
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

write_json('classified.json', classified_array)
c.close()

print(t.contents)
