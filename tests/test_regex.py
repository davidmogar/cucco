# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import os
import re
import sys

# Add sources to path
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../')

from cucco import regex

with open('tests/test_cases.json', 'r') as data:
    TESTS_DATA = json.load(data)

class TestRegex:

    @staticmethod
    def _find_all(pattern, string):
        return [x[0] if isinstance(x, tuple) else x for x in re.findall(pattern=pattern, string=string)]

    @staticmethod
    def _tests_generator(test):
        for test in TESTS_DATA['tests'][test[5:]]:
            yield test['message'], test['text'], test['values']

    def test_find_urls(self, request):
        for message, text, values in self._tests_generator(request.node.name):
            assert self._find_all(regex.URL_REGEX, text) == values, message

    def test_find_emails(self, request):
        for message, text, values in self._tests_generator(request.node.name):
            assert self._find_all(regex.EMAIL_REGEX, text) == values, message
