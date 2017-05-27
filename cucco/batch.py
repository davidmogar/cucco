from __future__ import absolute_import

import os

BATCH_EXTENSION = '.cucco'


class Batch(object):

    def	__init__(self, config, cucco):
        """Inits Batch class."""
        self.__config = config
        self.__cucco = cucco
        self.__logger = config.logger

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
        output_path = '%s%s' % (path, BATCH_EXTENSION)

        with open(output_path, 'w') as file:
            for line in self._line_generator(path):
                file.write('%s\n' % self.__cucco.normalize(line))

        if self.__config.debug:
            self.__logger.debug('Created file %s', output_path)

    def process_files(self, path, recursive=False):
        self.__logger.info('Processing files in %s', path)

        for (path, file) in self._file_generator(path, recursive):
            if not file.endswith(BATCH_EXTENSION):
                file_path = os.path.join(path, file)

                if self.__config.verbose:
                    self.__logger.info('Processing file %s', file_path)

                self._process_file(file_path)

    def watch(self, path):
        pass
