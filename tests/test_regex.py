# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import unittest

from normalizr import regex


def findall_simple(pattern, string):
    return [x[0] if isinstance(x, tuple) else x for x in re.findall(pattern=pattern, string=string)]


class TestRegex(unittest.TestCase):
    def test_find_urls(self):
        test_cases = [
            # (text, list of urls in text)
            {
                'name': 'empty string',
                'text': "",
                'urls': []
            },
            {
                'name': 'normalizr docs',
                'text': "http://normalizr.readthedocs.io/en/stable/",
                'urls': ["http://normalizr.readthedocs.io/en/stable/"]
            },
        ]

        for test_case in test_cases:
            name, text, urls = test_case['name'], test_case['text'], test_case['urls']
            self.assertListEqual(findall_simple(regex.URL_REGEX, text), urls)

    def test_find_emails(self):
        test_cases = [
            # (text, list of emails in text)
            {
                'name': 'empty string',
                'text': "",
                'emails': []
            },
            {
                'name': 'david mogar',
                'text': "david.mogar@gmail.com",
                'emails': ["david.mogar@gmail.com"]
            },
        ]

        for test_case in test_cases:
            name, text, emails = test_case['name'], test_case['text'], test_case['emails']
            self.assertListEqual(findall_simple(regex.EMAIL_REGEX, text), emails)


if __name__ == '__main__':
    unittest.main()
