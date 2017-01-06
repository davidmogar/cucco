# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys
import six

from normalizr import normalizr

if six.PY3:
    import unittest
else:
    import unittest2 as unittest

if six.PY2:
    from codecs import open


def read_file(path, encoding='utf-8'):
    """Read text from file."""
    with open(path, encoding=encoding) as f:
        return f.read()


class TestNormalizr(unittest.TestCase):
    _normalizr = None

    def setUp(self):
        self._normalizr = normalizr.Normalizr()

    def _fail_message(self, test_name):
        return "failed in sub-test: %s" % test_name

    def test_remove_accent_marks(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'after': ""
            },
            {
                'name': 'wikipedia italian',
                'before': "Wikipedia è un'enciclopedia online, collaborativa e culturalmente libera.",
                'after': "Wikipedia e un'enciclopedia online, collaborativa e culturalmente libera."
            },
        ]

        for test_case in test_cases:
            name, before, after = test_case['name'], test_case['before'], test_case['after']
            self.assertEqual(self._normalizr.remove_accent_marks(before), after, msg=self._fail_message(name))

    def test_remove_extra_whitespaces(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'after': ""
            },
            {
                'name': 'no extra whitespaces',
                'before': "Who let the dog out?",
                'after': "Who let the dog out?"
            },
            {
                'name': 'new line',
                'before': "Who let\nthe dog out?",
                'after': "Who let the dog out?"
            },
            {
                'name': 'double space',
                'before': "Who let  the dog out?",
                'after': "Who let the dog out?"
            },
            {
                'name': 'strip',
                'before': " Who let  the dog out? ",
                'after': "Who let the dog out?"
            },
            {
                'name': 'complex',
                'before': "  Who\tlet \n the dog out?\n\n\n\t",
                'after': "Who let the dog out?"
            },
        ]

        for test_case in test_cases:
            name, before, after = test_case['name'], test_case['before'], test_case['after']
            self.assertEqual(self._normalizr.remove_extra_whitespaces(before), after, msg=self._fail_message(name))

    def test_replace_emojis(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'after': ""
            },
            {
                'name': 'no emoji',
                'before': "Grinning Face",
                'after': "Grinning Face"
            },
            {
                'name': 'smiley default replacement',
                'before': "😀 Grinning Face",
                'after': " Grinning Face"
            },
            {
                'name': 'smiley custom replacement',
                'before': "😀 Grinning Face",
                'kwargs': {'replacement': ':-)'},
                'after': ":-) Grinning Face"
            },
        ]

        for test_case in test_cases:
            name, before, kwargs, after = \
                test_case['name'], test_case['before'], test_case.get('kwargs', dict()), test_case['after']
            self.assertEqual(self._normalizr.replace_emojis(text=before, **kwargs), after, msg=self._fail_message(name))

    def test_replace_hyphens(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'after': ""
            },
            {
                'name': 'no hyphens',
                'before': "New York",
                'after': "New York"
            },
            {
                'name': 'hyphen default replacement',
                'before': "New-York",
                'after': "New York"
            },
            {
                'name': 'hyphen custom replacement',
                'before': "New-York",
                'kwargs': {'replacement': '_'},
                'after': "New_York"
            },
        ]

        for test_case in test_cases:
            name, before, kwargs, after = \
                test_case['name'], test_case['before'], test_case.get('kwargs', dict()), test_case['after']
            self.assertEqual(self._normalizr.replace_hyphens(text=before, **kwargs), after, msg=self._fail_message(name))

    def test_replace_punctuation(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'after': ""
            },
            {
                'name': 'no punctuation',
                'before': "Who let the dog out",
                'after': "Who let the dog out"
            },
            {
                'name': 'question mark default replacement',
                'before': "Who let the dog out?",
                'after': "Who let the dog out"
            },
            {
                'name': 'question mark custom replacement',
                'before': "Who let the dog out?",
                'kwargs': {'replacement': ' '},
                'after': "Who let the dog out "
            },
            {
                'name': 'simple sentence default replacement',
                'before': "With normalizr you can replace symbols, punctuation, remove stop words and much more.",
                'after': "With normalizr you can replace symbols punctuation remove stop words and much more"
            },
            {
                'name': 'simple sentence custom replacement',
                'before': "With normalizr you can replace symbols, punctuation, remove stop words and much more.",
                'kwargs': {'replacement': '_'},
                'after': "With normalizr you can replace symbols_ punctuation_ remove stop words and much more_"
            },
            {
                'name': 'simple sentence dot excluded',
                'before': "With normalizr you can replace symbols, punctuation, remove stop words and much more.",
                'kwargs': {'excluded': {'.'}},
                'after': "With normalizr you can replace symbols punctuation remove stop words and much more."
            },
        ]

        for test_case in test_cases:
            name, before, kwargs, after = \
                test_case['name'], test_case['before'], test_case.get('kwargs', dict()), test_case['after']
            self.assertEqual(self._normalizr.replace_punctuation(text=before, **kwargs), after,
                             msg=self._fail_message(name))

    def test_replace_characters(self):
        test_cases = [
            {
                'name': 'empty string',
                'before': "",
                'characters': "",
                'after': ""
            },
            {
                'name': 'no characters',
                'before': "Who let the dog out?",
                'characters': "",
                'after': "Who let the dog out?"
            },
            {
                'name': 'vowels',
                'before': "Who let the dog out?",
                'characters': "aeiouAEIOU",
                'after': "Wh lt th dg t?"
            },
            {
                'name': 'vowels to _',
                'before': "Who let the dog out?",
                'characters': "aeiouAEIOU",
                'kwargs': {'replacement': "_"},
                'after': "Wh_ l_t th_ d_g __t?"
            },
            {
                'name': 'question mark',
                'before': "Who let the dog out?",
                'characters': "?",
                'after': "Who let the dog out"
            },
            {
                'name': 'question mark to exclamation mark',
                'before': "Who let the dog out?",
                'characters': "?",
                'kwargs': {'replacement': "!"},
                'after': "Who let the dog out!"
            },
        ]

        for test_case in test_cases:
            name, before, characters, kwargs, after = \
                test_case['name'], test_case['before'], test_case['characters'], test_case.get('kwargs', dict()), \
                test_case['after']
            self.assertEqual(self._normalizr.replace_characters(text=before, characters=characters, **kwargs), after,
                             msg=self._fail_message(name))


if __name__ == '__main__':
    unittest.main()
