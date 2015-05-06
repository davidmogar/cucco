import os
import string
import unicodedata

path = os.path.dirname(__file__)


class Normalizr:
    __stop_words = set()

    def __init__(self, language='en'):
        self._load_stop_words(language)

    def _load_stop_words(self, language):
        with open(os.path.join(path, 'data/stop-' + language), 'r') as file:
            for line in file:
                fields = line.split('|')
                if fields:
                    word = fields[0].strip()
                    if word: self.__stop_words.add(word)

    def normalize(self, text, normalizations=None):
        if normalizations is None:
            normalizations = ['whitespaces', 'punctuation', 'accents', 'symbols', 'stopwords']

        methods = {
            'accents': self.remove_accent_marks(text),
            'hyphens': self.replace_hyphens(text),
            'punctuation': self.remove_punctuation(text),
            'stopwords': self.remove_stop_words(text),
            'symbols': self.remove_symbols(),
            'whitespaces': self.remove_extra_whitespaces(text)
        }

        for normalization in normalizations:
            text = methods[normalization]

        return text


    def remove_accent_marks(self, text, format='NFKD', excluded=set()):
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) != 'Mn' or c in excluded)

    def remove_extra_whitespaces(self, text):
        return ' '.join(text.strip().split())

    def replace_hyphens(self, text, replacement=' '):
        return text.replace('-', replacement)

    def remove_punctuation(self, text):
        return ''.join(c for c in text if c not in string.punctuation)

    def remove_stop_words(self, text, ignore_case=False):
        return ' '.join(
            word for word in text.split(' ') if (word.lower() if ignore_case else word) not in self.__stop_words)

    def remove_symbols(self, text, format='NFKD', excluded=set()):
        categories = set(['Mn', 'Sc', 'Sk', 'Sm', 'So'])
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) not in categories or c in excluded)