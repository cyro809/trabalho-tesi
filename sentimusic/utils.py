#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re

def remove_special_characters(text):
    text = text.strip()
    text = text.replace('\n\n', ' ')
    text = text.replace('\n', ' ')
    text = re.sub('[!,.()?]', ' ', text)
    return text
