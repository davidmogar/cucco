from __future__ import absolute_import

import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BATCH_EXTENSION = '.cucco'

def files_generator(path, recursive):
    """Yield files found in a given path.

    Walk over a given path finding and yielding all
    files found on it. This can be done only on the root
    directory or recursively.

    Args:
        path: Path to the directory.
        recursive: Whether to find files recursively or not.

    Yields:
        A tuple for each file in the given path containing
        the path and the name of the file.
    """
    if recursive:
        for (path, _, files) in os.walk(path):
            for file in files:
                if not file.endswith(BATCH_EXTENSION):
                    yield (path, file)
    else:
        for file in os.listdir(path):
            if (os.path.isfile(os.path.join(path, file)) and
                    not file.endswith(BATCH_EXTENSION)):
                yield (path, file)

def lines_generator(path):
    """Yield lines in a given file.

    Iterates over a file lines yielding them.

    Args:
        path: Path to the file.

    Yields:
        Lines on a given file.
    """
    with open(path, 'r') as file:
        for line in file:
            yield line


class Batch(object):
    """Class to apply normalizations in batch mode.

    This class permits to apply normalizations over a group
    of files. It counts with two modes. The first one works
    over all the files in a directory and the second one
    watch for new files in a given path. Both modes generate
    new files with the result of the normalizations, letting
    the original files unchanged.

    Attributes:
        config: Config to use.
        cucco: Reference to cucco object.
   """

    def	__init__(self, config, cucco):
        """Inits Batch class."""
        self._config = config
        self._cucco = cucco
        self._logger = config.logger
        self._observer = None
        self._watch = False

    def process_file(self, path):
        """Process a file applying normalizations.

        Get a file as input and generate a new file with the
        result of applying normalizations to every single line
        in the original file. The extension for the new file
        will be the one defined in BATCH_EXTENSION.

        Args:
            path: Path to the file.
        """
        if self._config.verbose:
            self._logger.info('Processing file "%s"', path)

        output_path = '%s%s' % (path, BATCH_EXTENSION)

        with open(output_path, 'w') as file:
            for line in lines_generator(path):
                file.write('%s\n' % self._cucco.normalize(
                           line.encode().decode('utf-8')))

        self._logger.debug('Created file "%s"', output_path)

    def process_files(self, path, recursive=False):
        """Apply normalizations over all files in the given directory.

        Iterate over all files in a given directory. Normalizations
        will be applied to each file, storing the result in a new file.
        The extension for the new file will be the one defined in
        BATCH_EXTENSION.

        Args:
            path: Path to the directory.
            recursive: Whether to find files recursively or not.
        """
        self._logger.info('Processing files in "%s"', path)

        for (path, file) in files_generator(path, recursive):
            if not file.endswith(BATCH_EXTENSION):
                self.process_file(os.path.join(path, file))

    def stop_watching(self):
        """Stop watching for files.

        Stop the observer started by watch function and finish
        thread life.
        """
        self._watch = False

        if self._observer:
            self._logger.info('Stopping watcher')
            self._observer.stop()
            self._logger.info('Watcher stopped')

    def watch(self, path, recursive=False):
        """Watch for files in a directory and apply normalizations.

        Watch for new or changed files in a directory and apply
        normalizations over them.

        Args:
            path: Path to the directory.
            recursive: Whether to find files recursively or not.
        """
        self._logger.info('Initializing watcher for path "%s"', path)

        handler = FileHandler(self)
        self._observer = Observer()
        self._observer.schedule(handler, path, recursive)

        self._logger.info('Starting watcher')
        self._observer.start()
        self._watch = True

        try:
            self._logger.info('Waiting for file events')
            while self._watch:
                time.sleep(1)
        except KeyboardInterrupt: # pragma: no cover
            self.stop_watching()

        self._observer.join()


class FileHandler(FileSystemEventHandler):
    """Handler to use by Batch watcher.

    This class is used by Batch's watch mode. The handler will
    listen for new and changed files.

    Attributes:
        batch: Reference to Batch object.
    """

    def __init__(self, batch):
        """Inits Batch class."""
        self._batch = batch
        self._logger = batch._logger

    def _process_event(self, event):
        """Process received events.

        Process events received, applying normalization for those
        events referencing a new or changed file and only if it's
        not the result of a previous normalization.

        Args:
            event: Event to process.
        """
        if (not event.is_directory and
                not event.src_path.endswith(BATCH_EXTENSION)):
            self._logger.info('Detected file change: %s', event.src_path)
            self._batch.process_file(event.src_path)

    def on_created(self, event):
        """Function called everytime a new file is created.

        Args:
            event: Event to process.
        """
        self._logger.debug('Detected create event on watched path: %s', event.src_path)

        self._process_event(event)

    def on_modified(self, event):
        """Function called everytime a new file is modified.

        Args:
            event: Event to process.
        """
        self._logger.debug('Detected modify event on watched path: %s', event.src_path)

        self._process_event(event)
