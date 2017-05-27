from __future__ import absolute_import, unicode_literals

import codecs
import logging
import os
import re
import string
import sys
import unicodedata

import cucco.regex as regex

from cucco.config import Config

PATH = os.path.dirname(__file__)


class Cucco(object):
    """This class offers methods for text normalization.

    Attributes:
        config: Config to use.
        lazy_load: Whether or not to lazy load files.
    """
    __punctuation = set(string.punctuation)

    def __init__(
            self,
            config=None,
            lazy_load=False):
        self.__config = config if config else Config()

        self.__characters_regexes = dict()
        self.__logger = self.__config.logger
        self.__stop_words = set()

        if not lazy_load:
            self._load_stop_words(self.__config.language)

    def _load_stop_words(self, language):
        """Load stop words into __stop_words set.

        Stop words will be loaded according to the language code
        received during instantiation.

        Args:
            language: Language code.
        """
        self.__logger.debug('Loading stop words')

        file_path = 'data/stop-' + language
        if not os.path.isfile(file_path):
            file_path = 'data/stop-en'

        with codecs.open(os.path.join(PATH, file_path),
                         'r', 'UTF-8') as file:
            for word in file:
                self.__stop_words.add(word.strip())

    @staticmethod
    def _parse_normalizations(normalizations):
        """Parse and yield normalizations.

        Parse normalizations parameter yielding all normalizations and
        arguments found on it.

        Args:
            normalizations: List of normalizations.

        Yields:
            A tuple with a parsed normalization. The first item will
            contain the normalization name and the second will be a dict
            with the arguments to use for the normalization.
        """
        str_type = str if sys.version_info[0] > 2 else (str, unicode)

        for normalization in normalizations:
            yield (normalization, {}) if isinstance(normalization, str_type) else normalization

    def normalize(self, text, normalizations=None):
        """Normalize a given text applying all normalizations.

        Normalizations to apply can be specified through a list
        parameter and will be executed in the same order.

        Args:
            text: The text to be processed.
            normalizations: List of normalizations to apply.

        Returns:
            The text normalized.
        """
        for normalization, kwargs in self._parse_normalizations(
                normalizations or self.__config.normalizations):
            text = getattr(self, normalization)(text, **kwargs)

        return text

    @staticmethod
    def remove_accent_marks(text, excluded=None):
        """Remove accent marks from input text.

        This function remove accent marks in the text, leaving
        untouched unicode characters defined in the 'excluded'
        parameter.

        Args:
            text: The text to be processed.
            excluded: Set of unicode characters to exclude.

        Returns:
            The text without accent marks.
        """
        if excluded is None:
            excluded = set()

        return unicodedata.normalize(
            'NFKC', ''.join(
                c for c in unicodedata.normalize(
                    'NFKD', text) if unicodedata.category(c) != 'Mn' or c in excluded))

    @staticmethod
    def remove_extra_whitespaces(text):
        """Remove extra white spaces from input text.

        This function removes white spaces from the beginning and
        the end of the string, but also duplicated white spaces
        between words.

        Args:
            text: The text to be processed.

        Returns:
            The text without extra white spaces.
        """
        return ' '.join(text.split())

    def remove_stop_words(self, text, ignore_case=True):
        """Remove stop words.

        Stop words are loaded on class instantiation according
        with the specified language.

        Args:
            text: The text to be processed.
            ignore_case: Whether or not ignore case.

        Returns:
            The text without stop words.
        """
        if not self.__stop_words:
            self._load_stop_words(self.__config.language)

        return ' '.join(word for word in text.split(' ') if (
            word.lower() if ignore_case else word) not in self.__stop_words)

    def replace_characters(self, text, characters, replacement=''):
        """Remove characters from text.

        Remove custom characters from input text or replace them
        with a string if specified.

        Args:
            text: The text to be processed.
            characters: Characters that will be replaced.
            replacement: New text that will replace the custom characters.

        Returns:
            The text without the given characters.
        """
        if not characters:
            return text

        characters = ''.join(sorted(characters))
        if characters in self.__characters_regexes:
            characters_regex = self.__characters_regexes[characters]
        else:
            characters_regex = re.compile("[%s]" % re.escape(characters))
            self.__characters_regexes[characters] = characters_regex

        return characters_regex.sub(replacement, text)

    @staticmethod
    def replace_emails(text, replacement=''):
        """Remove emails address from text.

        Remove email addresses from input text or replace them
        with a string if specified.

        Args:
            text: The text to be processed.
            replacement: New text that will replace email addresses.

        Returns:
            The text without email addresses.
        """
        return re.sub(regex.EMAIL_REGEX, replacement, text)

    @staticmethod
    def replace_emojis(text, replacement=''):
        """Remove emojis from text.

        Remove emojis from input text or replace them with a
        string if specified.

        Args:
            text: The text to be processed.
            replacement: New text that will replace emojis.

        Returns:
            The text without hyphens.
        """
        return regex.EMOJI_REGEX.sub(replacement, text)

    @staticmethod
    def replace_hyphens(text, replacement=' '):
        """Replace hyphens in text.

        Replace hyphens from input text with a whitespace or a
        string if specified.

        Args:
            text: The text to be processed.
            replacement: New text that will replace hyphens.

        Returns:
            The text without hyphens.
        """
        return text.replace('-', replacement)

    def replace_punctuation(self, text, excluded=None, replacement=''):
        """Replace punctuation symbols in text.

        Remove punctuation from input text or replace them with a
        string if specified. Characters replaces will be those
        in string.punctuation.

        Args:
            text: The text to be processed.
            excluded: Set of characters to exclude.
            replacement: New text that will replace punctuation.

        Returns:
            The text without punctuation.
        """
        if excluded is None:
            excluded = set()
        elif not isinstance(excluded, set):
            excluded = set(excluded)
        punct = ''.join(self.__punctuation.difference(excluded))

        return self.replace_characters(
            text, characters=punct, replacement=replacement)

    @staticmethod
    def replace_symbols(
            text,
            form='NFKD',
            excluded=None,
            replacement=''):
        """Replace symbols in text.

        Remove symbols from input text or replace them with a
        string if specified.

        Args:
            text: The text to be processed.
            form: Unicode form.
            excluded: Set of unicode characters to exclude.
            replacement: New text that will replace symbols.

        Returns:
            The text without symbols.
        """
        if excluded is None:
            excluded = set()

        categories = set(['Mn', 'Sc', 'Sk', 'Sm', 'So'])

        return ''.join(c if unicodedata.category(c) not in categories or c in excluded
                       else replacement for c in unicodedata.normalize(form, text))

    @staticmethod
    def replace_urls(text, replacement=''):
        """Replace URLs in text.

        Remove URLs from input text or replace them with a
        string if specified.

        Args:
            text: The text to be processed.
            replacement: New text that will replace URLs.

        Returns:
            The text without URLs.
        """
        return re.sub(regex.URL_REGEX, replacement, text)
