class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ConfigError(Error):
    """Exception raised for errors loading config file.

    Attributes:
        message: Explanation of the error.
    """

    def __init__(self, message):
        self.message = message
