# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import pytest
import sys

# Add sources to path
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../')

from cucco.config import Config
from cucco.config import DEFAULT_NORMALIZATIONS
from cucco.errors import ConfigError

STR_TYPE = str if sys.version_info[0] > 2 else (str, unicode)

class TestConfig(object):

    @pytest.fixture
    def config(cls):
        return Config()

    def test_init(self):
        config = Config(normalizations=DEFAULT_NORMALIZATIONS)
        assert isinstance(config.normalizations, list), \
                'normalizations should be a list'
        assert len(config.normalizations) == 4, \
                'normalizations should be a list of 4 elements'

        config = Config(normalizations='tests/files/config_valid.yaml')
        assert isinstance(config.normalizations, list), \
                'normalizations should be a list'
        assert len(config.normalizations) == 3, \
                'normalizations should be a list of 3 elements'

    def test_load_from_file(self, config):
        with pytest.raises(ConfigError) as e:
            config._load_from_file('invalid path')
        assert 'Problem while loading file' in str(e.value.message)

        with pytest.raises(ConfigError) as e:
            config._load_from_file('tests/files/config_empty.yaml')
        assert 'unexpected structure' in str(e.value.message)

        with pytest.raises(ConfigError) as e:
            config._load_from_file('tests/files/config_invalid_key.yaml')
        assert 'unexpected structure' in str(e.value.message)

        with pytest.raises(ConfigError) as e:
            config._load_from_file('tests/files/config_invalid.yaml')
        assert 'Invalid YAML' in str(e.value.message)

        result = config._load_from_file('tests/files/config_valid.yaml')
        assert isinstance(result, list), \
                'normalizations should be a list'
        assert len(result) == 3, \
                'normalizations should be a list of 3 elements'

        for normalization in result:
            assert (isinstance(normalization, dict) or
                    isinstance(normalization, STR_TYPE)), \
                'all normalizations should be dictionaries'

        assert list(result[0].keys())[0] == 'remove_extra_whitespaces', \
                'first normalization should be remove_extra_whitespaces'

    def test_parse_normalization(self, config):
        assert config._parse_normalization(None) == None, \
                'normalization should be None when passing None'
        assert config._parse_normalization(('foo', 'bar')) == None, \
                'normalization should be None when passing a tuple'
        assert isinstance(config._parse_normalization('string'), STR_TYPE), \
                'normalization should be string when passing an string'
        assert isinstance(config._parse_normalization({ 'foo': 'bar' }), STR_TYPE), \
                'normalization should be string when passing a simple dict'
        assert isinstance(config._parse_normalization({ 'foo': ['bar'] }), STR_TYPE), \
                'normalization should be string when passing invalid options structures'

        # Normalization with options
        result = config._parse_normalization({ 'foo': {'bar': 'baz', 'baz': 'bar'} })
        assert isinstance(result, tuple), \
                'options normalization should be tuple when passing a dict'
        assert len(result) == 2, \
                'options normalization tuple should have 2 elements'
        assert isinstance(result[1], dict), \
                'options normalization second element should be a dict'
        assert len(result[1]) == 2, \
                'options normalization should have two options'

    def test_parse_normalizations(self, config):
        with pytest.raises(ConfigError):
            config._parse_normalizations('not list')

        result = config._parse_normalizations(
                [ 'foo', { 'bar': {'bar': 'baz', 'baz': 'bar'} }, 'baz' ])
        assert isinstance(result, list), \
                'normalizations should be a list'
        assert len(result) == 3, \
                'normalizations list should have 3 elements'
        assert isinstance(result[0], STR_TYPE), \
                'normalizations first element should be a string'
        assert isinstance(result[1], tuple), \
                'normalizations second element should be a tuple'
        assert len(result[1]) == 2, \
                'normalizations second element should have two options'
        assert isinstance(result[2], STR_TYPE), \
                'normalizations third element should be a string'


