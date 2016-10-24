from __future__ import absolute_import

import codecs
import logging
import os
import re
import string
import sys
import unicodedata
import sys

import normalizr.regex as regex

path = os.path.dirname(__file__)

IS_PY3 = sys.version_info[0] == 3

DEFAULT_NORMALIZATIONS = [
    'remove_extra_whitespaces', 'replace_punctuation', 'replace_symbols', 'remove_stop_words'
]


def string_translate(s, from_chars='', to_chars='', del_chars=''):
    if IS_PY3:
        return s.translate(str.maketrans(from_chars, to_chars, del_chars))
    else:
        if isinstance(s, unicode):
            trans = dict(zip(from_chars, to_chars))
            trans.update(dict.fromkeys(del_chars))
            return s.translate(trans)
        else:
            return s.translate(string.maketrans(from_chars, to_chars), del_chars)


class Normalizr:
    """
    This class offers methods for text normalization.

    Attributes:
        language (string): Language used for normalization.
        lazy_load (boolean): Whether or not lazy load files.
    """
    __punctuation = string.punctuation

    def __init__(self, language='en', lazy_load=False, logger_level=logging.INFO):
        self.__language = language
        self.__logger = self._get_logger(logger_level)
        self.__stop_words = set()

        if not lazy_load:
            self._load_stop_words(language)

    def _get_logger(self, level):
        """
        Initialize logger.

        Params:
            level (integer): Log level as defined in logging.
        """
        logging.basicConfig()
        logger = logging.getLogger("Normalizr")
        logger.setLevel(level)

        return logger

    def _load_stop_words(self, language):
        """
        Load stop words into __stop_words set.

        Stop words will be loaded according to the language code received during instantiation.

        Params:
            language (string): Language code.
        """
        self.__logger.debug('loading stop words')
        with codecs.open(os.path.join(path, 'data/stop-' + language), 'r', 'UTF-8') as file:
            for line in file:
                fields = line.split('|')
                if fields:
                    for word in fields[0].split(): self.__stop_words.add(word.strip())

    def _parse_normalizations(self, normalizations):
        for normalization in normalizations:
            yield (normalization, {}) if isinstance(normalization, str) else normalization

    def normalize(self, text, normalizations=None):
        """
        Normalize a given text applying all normalizations.

        Normalizations to apply can be specified through a list parameter and will be executed
        in the same order.

        Params:
            text (string): The text to be processed.
            normalizations (list): List of normalizations to apply.

        Returns:
            The text normalized.
        """
        for normalization, kwargs in self._parse_normalizations(normalizations or DEFAULT_NORMALIZATIONS):
            text = getattr(self, normalization)(text, **kwargs)
        return text

    def remove_accent_marks(self, text, excluded=set()):
        """
        Remove accent marks from input text.

        Params:
            text (string): The text to be processed.
            excluded (set): Set of unicode characters to exclude.

        Returns:
            The text without accent marks.
        """
        return unicodedata.normalize('NFKC', ''.join(c for c in unicodedata.normalize('NFKD', text)
                       if unicodedata.category(c) != 'Mn' or c in excluded))

    def remove_extra_whitespaces(self, text):
        """
        Remove extra whitespaces from input text.

        This function removes whitespaces from the beginning and the end of
        the string, but also duplicated whitespaces between words.

        Params:
            text (string): The text to be processed.

        Returns:
            The text without extra whitespaces.
        """
        return ' '.join(text.split())

    def remove_stop_words(self, text, ignore_case=True):
        """
        Remove stop words.

        Stop words are loaded on class instantiation according with the specified language.

        Params:
            text (string): The text to be processed.
            ignore_case (boolean): Whether or not ignore case.

        Returns:
            The text without stop words.
        """
        if not self.__stop_words:
            self._load_stop_words(self.__language)

        return ' '.join(
            word for word in text.split(' ') if (word.lower() if ignore_case else word) not in self.__stop_words)

    def replace_emojis(self, text, replacement=''):
        """
        Remove emojis from input text or replace them with a string if specified.

        Params:
            text (string): The text to be processed.
            replacement (string): New text that will replace emojis.

        Returns:
            The text without hyphens.
        """
        try:
            highpoints = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
            highpoints = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')

        return highpoints.sub(replacement, text)

    def replace_hyphens(self, text, replacement=' '):
        """
        Replace hyphens from input text with a whitespace or a string if specified.

        Params:
            text (string): The text to be processed.
            replacement (string): New text that will replace hyphens.

        Returns:
            The text without hyphens.
        """
        return text.replace('-', replacement)

    def replace_punctuation(self, text, excluded=set(), replacement=''):
        """
        Remove punctuation from input text or replace them with a string if specified.

        This function will remove characters from string.punctuation.

        Params:
            text (string): The text to be processed.
            excluded (set): Set of characters to exclude.
            replacement (string): New text that will replace punctuation.

        Returns:
            The text without punctuation.
        """
        punct = string_translate(self.__punctuation, del_chars=''.join(excluded))
        return self.replace_characters(text, characters=punct, replacement=replacement)

    def replace_symbols(self, text, format='NFKD', excluded=set(), replacement=''):
        """
        Remove symbols from input text or replace them with a string if specified.

        Params:
            text (string): The text to be processed.
            format (string): Unicode format.
            excluded (set): Set of unicode characters to exclude.
            replacement (string): New text that will replace symbols.

        Returns:
            The text without symbols.
        """
        categories = set(['Mn', 'Sc', 'Sk', 'Sm', 'So'])
        return ''.join(c if unicodedata.category(c) not in categories or c in excluded else replacement
                       for c in unicodedata.normalize(format, text))

    def replace_characters(self, text, characters, replacement=''):
        """
        Remove custom characters from input text or replace them with a string if specified.

        Params:
            text (string): The text to be processed.
            characters (string): Characters that will be replaced.
            replacement (string): New text that will replace the custom characters.

        Returns:
            The text without the given characters.
        """
        # exit if nothing to replace
        if not characters:
            # TODO: consider raising a warning here
            return text

        if not replacement:
            return string_translate(text, del_chars=characters)

        replacement_char = characters[0]

        if len(characters) > 2:
            characters = characters[1:]
            text = string_translate(text, from_chars=characters, to_chars=replacement_char * len(characters))

        return text.replace(replacement_char, replacement)

    def replace_urls(self, text, replacement=''):
        """
        Remove URLs from input text or replace them with a string if specified.

        Params:
            text (string): The text to be processed.
            replacement (string): New text that will replace URLs.

        Returns:
            The text without URLs.
        """
        return re.sub(regex.URL_REGEX, replacement, text)

    def replace_emails(self, text, replacement=''):
        """
        Remove email addresses from input text or replace them with a string if specified.

        Params:
            text (string): The text to be processed.
            replacement (string): New text that will replace email addresses.

        Returns:
            The text without email addresses.
        """
        return re.sub(regex.EMAIL_REGEX, replacement, text)
