# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import os
import pytest
import shutil
import sys
import time

from threading import Thread

# Add sources to path
PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../')

from cucco.batch import Batch
from cucco.batch import BATCH_EXTENSION
from cucco.batch import files_generator
from cucco.batch import lines_generator
from cucco.config import Config
from cucco.cucco import Cucco

BATCH_PATH = 'tests/files/batch'
WATCH_PATH = 'tests/files/watch'

def clean_up_files():
    if os.path.isdir(BATCH_PATH):
        for (path, dirs, files) in os.walk(BATCH_PATH):
            for file in files:
                if file.endswith(BATCH_EXTENSION):
                    os.remove(os.path.join(path, file))

    if os.path.isdir(WATCH_PATH):
        shutil.rmtree(WATCH_PATH)

def watch_directory(watched_file, recursive, batch):
    thread = Thread(target = batch.watch, args = (WATCH_PATH, recursive))
    thread.start()

    # Create a file once the watcher is ready
    time.sleep(1)
    with open(watched_file, 'w') as f:
        f.write('The line  1')

    current = datetime.datetime.now()
    limit = current + datetime.timedelta(seconds=20)

    while current < limit:
        if os.path.isfile('%s%s' % (watched_file, BATCH_EXTENSION)):
            break

        time.sleep(0.1)
        current = datetime.datetime.now()

    batch.stop_watching()


class TestConfig(object):

    @pytest.fixture
    def batch(cls):
        config = Config(debug=True, verbose=True)
        cucco = Cucco()

        return Batch(config, cucco)

    @classmethod
    def setup_class(cls):
        clean_up_files()

    @classmethod
    def teardown_class(cls):
        clean_up_files()

    def test_files_generator(self, batch):
        result = [ file for file in files_generator(BATCH_PATH, False) ]
        assert len(result) == 3, \
                'target directory should contain only three files'

        result = [ file for file in files_generator(BATCH_PATH, True) ]
        assert len(result) == 4, \
                'target directory should contain only four files'

    def test_lines_generator(self, batch):
        result = [ line for line in lines_generator('%s/batch_one_line' % BATCH_PATH) ]
        assert len(result) == 1, \
                'target file should contain exactly one line'

        result = [ line for line in lines_generator('%s/subdirectory/batch_four_lines' % BATCH_PATH) ]
        assert len(result) == 4, \
                'target file should contain exactly four lines'
        assert 'Line 3\n' in result, \
                'target file should contain "Line 3"'

    def test_process_file(self, batch):
        batch.process_file('%s/batch_one_line' % BATCH_PATH)
        assert os.path.isfile('%s/batch_one_line.cucco' % BATCH_PATH), \
                'normalized file should have been created'

        with open('%s/batch_one_line.cucco' % BATCH_PATH) as file:
            assert file.read() == 'line 1\n', \
                    'normalized file content should be " line 1"'

    def test_process_files(self, batch):
        batch.process_files(BATCH_PATH, False)
        result = [ file for file in os.listdir(BATCH_PATH) if file.endswith(BATCH_EXTENSION) ]
        assert len(result) == 3, \
                'target directory should contain only three files'

        batch.process_files(BATCH_PATH, True)
        result = []
        for (path, dirs, files) in os.walk(BATCH_PATH):
            for file in files:
                if file.endswith('.cucco'):
                    result.append(file)
        assert len(result) == 4, \
                'target directory should contain only four files'


    def test_watch(self, batch):
        if not os.path.isdir(WATCH_PATH):
            os.makedirs(WATCH_PATH)

        watch_directory('%s/watched_file' % WATCH_PATH, False, batch)

        assert os.path.isfile('%s/watched_file.cucco' % WATCH_PATH), \
                'normalized file should have been created'

        with open('%s/watched_file.cucco' % WATCH_PATH) as file:
            assert file.read() == 'line 1\n', \
                    'normalized file content should be " line 1"'

    def test_watch_recursive(self, batch):
        if not os.path.isdir(WATCH_PATH):
            os.makedirs(WATCH_PATH)
        subdirectory = '%s/subdirectory' % WATCH_PATH
        if not os.path.isdir(subdirectory):
            os.makedirs(subdirectory)

        watch_directory('%s/watched_file' % subdirectory, True, batch)

        assert os.path.isfile('%s/watched_file.cucco' % subdirectory), \
                'normalized file should have been created'

        with open('%s/watched_file.cucco' % subdirectory) as file:
            assert file.read() == 'line 1\n', \
                    'normalized file content should be " line 1"'
