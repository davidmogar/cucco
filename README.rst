.. image:: http://davidmogar.com/uploads/github/normalizr.png
   :align: middle
.. image:: https://img.shields.io/pypi/v/normalizr.svg
   :target: https://pypi.python.org/pypi/normalizr
   :align: right
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/davidmogar/normalizr/blob/master/LICENSE
   :align: right
.. image:: https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg
   :target: https://gitter.im/davidmogar/normalizr?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
   :align: right
   
Normalizr is a Python library for text normalization that allows the next actions:

-  Remove accents.
-  Remove extra whitespaces.
-  Remove hyphens.
-  Remove punctuation.
-  Remove stop words (from 13 different languages).
-  Remove symbols.

Supported languages
-------------------

At the moment, normalizr can remove stop words in these languages:

-  Danish (da)
-  Dutch (nl)
-  English (en, default)
-  Finnish (fi)
-  French (fr)
-  German (de)
-  Hungarian (hu)
-  Italian (it)
-  Norwegian (no)
-  Portuguese (pr)
-  Russian (ru)
-  Spanish (es)
-  Swedish (sv)

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
    print(normalizr.normalize('Who let the dog out?'))

Output:

.. code::

    let dog

It's also possible to send a list of normalizations to apply, which will be executed in order.

.. code:: python

    from normalizr import Normalizr

    normalizr = Normalizr(language='en')
    print(normalizr.normalize('Who    let   the dog out?', ['whitespaces', 'punctuation']))

Output:

.. code::

    Who let the dog out

If you only need to apply one normalization, use one of these methods:

-  remove_accent_marks
-  replace_hyphens
-  remove_punctuation
-  remove_stop_wordd
-  remove_symbols
-  remove_extra_whitespaces
