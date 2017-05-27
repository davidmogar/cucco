from __future__ import absolute_import

import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BATCH_EXTENSION = '.cucco'


class Batch(object):

    def	__init__(self, config, cucco):
        """Inits Batch class."""
        self._config = config
        self._logger = config.logger

        self.__cucco = cucco

    def _file_generator(self, path, recursive):
        if recursive:
            for (path, dirs, files) in os.walk(path):
                for file in files:
                    yield (path, file)
        else:
            for file in os.listdir(path):
                yield (path, file)

    def _line_generator(self, path):
        with open(path, 'r') as file:
            for line in file:
                yield line

    def _process_file(self, path):
        if self._config.verbose:
            self._logger.info('Processing file "%s"', path)

        output_path = '%s%s' % (path, BATCH_EXTENSION)

        with open(output_path, 'w') as file:
            for line in self._line_generator(path):
                file.write('%s\n' % self.__cucco.normalize(line))

        if self._config.debug:
            self._logger.debug('Created file "%s"', output_path)

    def _start_watcher(self, observer):
        self._logger.info('Starting watcher')
        observer.start()

        try:
            self._logger.info('Waiting for file events')
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self._logger.info('Stopping watcher')
            observer.stop()
            self._logger.info('Watcher stopped')

        observer.join()

    def process_files(self, path, recursive=False):
        self._logger.info('Processing files in "%s"', path)

        for (path, file) in self._file_generator(path, recursive):
            if not file.endswith(BATCH_EXTENSION):
                self._process_file(os.path.join(path, file))

    def watch(self, path, recursive=False):
        self._logger.info('Initializing watcher for path "%s"', path)

        handler = FileHandler(self)
        observer = Observer()
        observer.schedule(handler, path, recursive)
        self._start_watcher(observer)


class FileHandler(FileSystemEventHandler):

    def __init__(self, batch):
        """Inits Batch class."""
        self.__batch = batch
        self.__debug = batch._config.debug
        self.__logger = batch._logger

    def _process_event(self, event):
        if (not event.is_directory and
                not event.src_path.endswith(BATCH_EXTENSION)):
            self.__logger.info('Detected file change: %s', event.src_path)
            self.__batch._process_file(event.src_path)

    def on_created(self, event):
        if self.__debug:
            self.__logger.debug('Detected create event on watched path: %s', event.src_path)

        self._process_event(event)

    def on_modified(self, event):
        if self.__debug:
            self.__logger.debug('Detected modify event on watched path: %s', event.src_path)

        self._process_event(event)
