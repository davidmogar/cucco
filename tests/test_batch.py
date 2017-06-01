# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import pytest
import sys

# Add sources to path
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../')

from cucco.batch import Batch
from cucco.config import Config
from cucco.cucco import Cucco

class TestConfig(object):

    @pytest.fixture
    def batch(cls):
        config = Config()
        cucco = Cucco()
        return Batch(config, cucco)

    @classmethod
    def teardown_class(cls):
        for (path, dirs, files) in os.walk('tests/files/batch'):
            for file in files:
                if file.endswith('cucco'):
                    os.remove(os.path.join(path, file))

    def test_file_generator(self, batch):
        result = [ file for file in batch._file_generator('tests/files/batch', False) ]
        assert len(result) == 3, \
                'target directory should contain only three files'

        result = [ file for file in batch._file_generator('tests/files/batch', True) ]
        assert len(result) == 4, \
                'target directory should contain only four files'

    def line_generator(self, batch):
        result = [ line for line in batch._line_generator('tests/files/batch/batch_one_line') ]
        assert len(result) == 1, \
                'target file should contain exactly one line'

        result = [ line for line in batch._line_generator('tests/files/batch/subdirectory/batch_four_line') ]
        assert len(result) == 4, \
                'target file should contain exactly four lines'
        assert 'Line three' in result, \
                'target file should contain "Line three"'

    def test_process_file(self, batch):
        batch._process_file('tests/files/batch/batch_one_line')
        assert os.path.isfile('tests/files/batch/batch_one_line.cucco'), \
                'normalized file should have been created'

        with open('tests/files/batch/batch_one_line.cucco') as file:
            assert file.read() == 'line 1\n', \
                    'normalized file content should be " line 1"'

    def test_process_files(self, batch):
        batch.process_files('tests/files/batch', False)
        result = [ file for file in os.listdir('tests/files/batch') if file.endswith('cucco') ]
        assert len(result) == 3, \
                'target directory should contain only three files'

        batch.process_files('tests/files/batch', True)
        result = []
        for (path, dirs, files) in os.walk('tests/files/batch'):
            for file in files:
                if file.endswith('.cucco'):
                    result.append(file)
        assert len(result) == 4, \
                'target directory should contain only four files'


    def test_watch(self, batch):
        pass
