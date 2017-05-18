from __future__ import absolute_import

import json
import sys
import yaml

DEFAULT_NORMALIZATIONS = [
    'remove_extra_whitespaces',
    'replace_punctuation',
    'replace_symbols',
    'remove_stop_words'
]
STR_TYPE = str if sys.version_info[0] > 2 else (str, unicode)


class Config(object):
    """
    This class offers functions to manage cucco configuration.
    """

    def	__init__(self, config=None):
        if config and not isinstance(config, list):
            config = self._load_from_file(config)
        else:
            config = DEFAULT_NORMALIZATIONS

        self.__normalizations = self._parse_normalizations(config)

    def _load_from_file(self, path):
        config = None

        try:
            with open(path, 'r') as config_file:
                config = yaml.load(config_file)['normalizations']
        except (EnvironmentError, yaml.YAMLError) as e:
            config = DEFAULT_NORMALIZATIONS

        return config

    def _parse_normalizations(self, config):
        normalizations = []

        for item in config:
            normalization = self._parse_normalization(item)
            if normalization:
                normalizations.append(normalization)

        return normalizations

    def _parse_normalization(self, item):
        """
        Parse a normalization item.

        If a dict is found, this is converted to a tuple given
        that it only contains a tuple. If string, the actual value
        is used.
        """
        normalization = None

        if isinstance(item, dict):
            if len(item.keys()) == 1:
                normalization = item.items()[0]
        elif isinstance(item, STR_TYPE):
            normalization = item

        return normalization
