
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import pycurl
import json

from urllib import urlencode

PY3 = sys.version_info[0] > 2


class Test:
    def __init__(self):
        self.contents = ''
        if PY3:
            self.contents = self.contents.encode('ascii')

    def body_callback(self, buf):
        self.contents = self.contents + buf


sys.stderr.write("Testing %s\n" % pycurl.version)

t = Test()
c = pycurl.Curl()
lyric = {
    'text': '''Give me all, give me all, give me all your attention baby\nI got to tell you a little something about yourself\nYou're wonderful, flawless, ooh you're a sexy lady\nBut you walk around here like you wanna be someone else\n\nI know that you don't know it, but you're fine, so fine\nOh girl I'm gonna show you when you're mine, oh mine\n\nTreasure, that is what you are\nHoney you're my golden star\nI know you can make my wish come true\nIf you let me treasure you\nIf you let me treasure you\n\nPretty girl, pretty girl, pretty girl you should be smiling\nA girl like you should never look so blue\nYou're everything I see in my dreams\nI wouldn't say that to you if it wasn't true\n\nI know that you don't know it, but you're fine, so fine\nOh girl I'm gonna show you when you're mine, oh mine\n\nTreasure, that is what you are\nHoney you're my golden star\nI know you can make my wish come true\nIf you let me treasure you\nIf you let me treasure you\n\nYou are my treasure, you are my treasure\nYou are my treasure, yeah, you you you, you are\nYou are my treasure, you are my treasure\nYou are my treasure, yeah, you you you, you are\n\nTreasure, that is what you are\nHoney you're my golden star\nI know you can make my wish come true\nIf you let me treasure you\nIf you let me treasure you'''
}
postfields = urlencode(lyric)
c.setopt(c.POSTFIELDS, postfields)
c.setopt(c.URL, 'http://text-processing.com/api/sentiment/')
c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
c.close()
result_dict = json.loads(t.contents)
print(t.contents)
