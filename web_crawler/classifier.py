#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import pycurl
import json

from urllib import urlencode

PY3 = sys.version_info[0] > 2

# ---------------------------------------------------------------------------
# Classe ClassifierResponse: Usada para retornar a resposta do Curl para classificar
# as músicas
# ---------------------------------------------------------------------------
class ClassifierResponse:
    def __init__(self):
        self.contents = ''
        if PY3:
            self.contents = self.contents.encode('ascii')

    def body_callback(self, buf):
        self.contents = self.contents + buf
