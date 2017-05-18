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
    Class to manage cucco configuration.

    This class allows to handle all cucco configuration and is
    used by the different modules.

    Attributes:
        normalizations: List or path to config file.
        verbose: Level of output verbosity.
    """

    normalizations = DEFAULT_NORMALIZATIONS

    def	__init__(self, normalizations=None, verbose=False):
        """Inits Confic class."""
        self.verbose = verbose

        if normalizations:
            if not isinstance(normalizations, list):
                normalizations = self._load_from_file(normalizations)

            self.normalizations = self._parse_normalizations(normalizations)

    def _load_from_file(self, path):
        """Load a config file from the given path.

        Load all normalizations from the config file received as
        argument. It expects to find a YAML file with a list of
        normalizations and arguments under the key 'normalizations'.

        Args:
            path: Path to YAML file.
        """
        config = []

        try:
            with open(path, 'r') as config_file:
                config = yaml.load(config_file)['normalizations']
        except EnvironmentError as e:
            print('Problem while loading file: %s' % e.args[1] if len(e.args) > 1 else e)
        except KeyError as e:
            print('key %s' % e)
        except yaml.YAMLError:
            print('yaml syntax not correct')

        return config

    def _parse_normalizations(self, normalizations):
        """Returns a list of parsed normalizations.

        Iterates over a list of normalizations, removing those
        not correctly defined. It also transform complex items
        to have a common format (list of tuples and strings).

        Args:
            normalizations: List of normalizations to parse.

        Returns:
            A list of normalizations after being parsed and curated.
        """
        parsed_normalizations = []

        for item in normalizations:
            normalization = self._parse_normalization(item)
            if normalization:
                parsed_normalizations.append(normalization)

        return parsed_normalizations

    def _parse_normalization(self, normalization):
        """Parse a normalization item.

        Transform dicts into a tuple containing the normalization
        options. If a string is found, the actual value is used.

        Args:
            normalization: Normalization to parse.

        Returns:
            Tuple or string containing the arsed normalization.
        """
        parsed_normalization = None

        if isinstance(normalization, dict):
            if len(normalization.keys()) == 1:
                parsed_normalization = normalization.items()[0]
        elif isinstance(normalization, STR_TYPE):
            parsed_normalization = normalization

        return parsed_normalization
