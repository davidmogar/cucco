normalizr
=========

Normalizr is a Python library for text normalization that allows the next actions:

- Remove accents.
- Remove extra whitespaces.
- Remove hyphens.
- Remove punctuation.
- Remove stop words (from 13 different languages).
- Remove symbols.

Installation
------------

The easiest way to install the latest version is by using pip to pull it
from `PyPI <https://pypi.python.org/pypi/normalizr>`_:

::

    pip install normalizr

You may also use Git to clone the repository from Github and install it
manually:

::

    git clone https://github.com/davidmogar/normalizr.git
    cd normalizr
    python setup.py install

Python 3.3 & 3.4 are supported.

Usage
-----

The next code shows a sample usage of this library:

.. code:: python

    from normalizr import Normalizr

    normalizr = Normalizr(language='en')
    print(normalizr.normalize('I love you'))

Output:

.. code::
    let dog