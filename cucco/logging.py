from __future__ import absolute_import

import logging

def initialize_logger(debug):
    """Set up logger to be used by the library.

    Args:
        debug: Wheter to use debug level or not
    """
    level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger('cucco')
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(levelname).1s %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
