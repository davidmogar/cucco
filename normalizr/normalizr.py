import codecs
import os
import re
import string
import unicodedata

import normalizr.regex as regex

path = os.path.dirname(__file__)

DEFAULT_NORMALIZATIONS = [
    'remove_extra_whitespaces', 'replace_punctuation', 'replace_symbols', 'remove_stop_words'
]


class Normalizr:
    """
    This class offers methods for text normalization.

    Attributes:
        language (string): Language used for normalization.
    """
    __punctuation = set(string.punctuation)
    __stop_words = set()

    def __init__(self, language='en'):
        self._load_stop_words(language)

    def _load_stop_words(self, language):
        """
        Load stop words into __stop_words set.

        Stop words will be loaded according to the language code received during instantiation.

        Params:
            language (string): Language code.
        """
        with codecs.open(os.path.join(path, 'data/stop-' + language), 'r', 'UTF-8') as file:
            for line in file:
                fields = line.split('|')
                if fields:
                    for word in fields[0].split(): self.__stop_words.add(word.strip())

    def normalize(self, text, normalizations=None):

        if normalizations is None:
            normalizations = ['whitespaces', 'punctuation', 'symbols', 'stopwords']

        methods = {
            'accents': self.remove_accent_marks,
            'hyphens': self.replace_hyphens,
            'punctuation': self.remove_punctuation,
            'stopwords': self.remove_stop_words,
            'symbols': self.remove_symbols,
            'whitespaces': self.remove_extra_whitespaces
        }

        for normalization in normalizations:
            text = methods[normalization](text)

        return text

    def _parse_normalizations(self, normalizations):
        for normalization in normalizations:
            if isinstance(normalization, str):
                kwargs = {}
            else:
                normalization, kwargs = normalization

            yield (normalization, kwargs)

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


    def remove_accent_marks(self, text, format='NFKD', excluded=set()):
        """
        Remove accent marks from input text.

        Params:
            text (string): The text to be processed.
            format (string): Unicode format.
            excluded (set): Set of unicode characters to exclude.

        Returns:
            The text without accent marks.
        """
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) != 'Mn' or c in excluded)

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
        return ' '.join(text.strip().split())

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

    def replace_punctuation(self, text, excluded=set(), replacement='',):
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
        return ''.join(c if c not in self.__punctuation or c in excluded else replacement for c in text)

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