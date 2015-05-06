import codecs
import os
import string
import unicodedata

path = os.path.dirname(__file__)


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
                    word = fields[0].strip()
                    if word: self.__stop_words.add(word)

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

    def replace_hyphens(self, text, replacement=' '):
        """
        Remove hyphens from input text.

        Params:
            text (string): The text to be processed.
            replacement (string): New text that will replace hyphens.

        Returns:
            The text without hyphens.
        """
        return text.replace('-', replacement)

    def remove_punctuation(self, text, excluded=set()):
        """
        Remove punctuation from input text.

        This function will remove characters from string.punctuation.

        Params:
            text (string): The text to be processed.
            excluded (set): Set of characters to exclude.

        Returns:
            The text without punctuation.
        """
        return ''.join(c for c in text if c not in self.__punctuation or c in excluded)

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

    def remove_symbols(self, text, format='NFKD', excluded=set()):
        """
        Remove symbols from input text.

        Params:
            text (string): The text to be processed.
            format (string): Unicode format.
            excluded (set): Set of unicode characters to exclude.

        Returns:
            The text without accent marks.
        """
        categories = set(['Mn', 'Sc', 'Sk', 'Sm', 'So'])
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) not in categories or c in excluded)