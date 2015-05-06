import string
import unicodedata


class Normalizr:
    def normalize(self, text):
        pass

    def remove_accent_marks(self, text, format='NFKD', excluded=set()):
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) != 'Mn' or c in excluded)

    def remove_extra_whitespaces(self, text):
        return ' '.join(text.strip().split())

    def replace_hyphens(self, text, replacement=' '):
        return text.replace('-', replacement)

    def remove_punctuation(self, text):
        return ''.join(c for c in text if c not in string.punctuation)

    def remove_symbols(self, text, format='NFKD', excluded=set()):
        categories = set(['Mn', 'Sc', 'Sk', 'Sm', 'So'])
        return ''.join(c for c in unicodedata.normalize(format, text)
                       if unicodedata.category(c) not in categories or c in excluded)