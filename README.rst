.. image:: https://github.com/davidmogar/normalizr/blob/master/normalizr.png

Normalizr is a Python library for text normalization that offers a bunch of actions to manipulate your text as much as you want. With normalizr you can replace symbols, punctuation, remove stop words and much more.


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

    normalizations = [
        'remove_extra_whitespaces',
        ('replace_punctuation', {'replacement': ' '})
    ]

    print(normalizr.normalize('Who    let   the dog out?', normalizations))

Output:

.. code::

    Who let the dog out

If you only need to apply one normalization, use one of these methods:

-  remove_accent_marks
-  remove_extra_whitespaces
-  remove_stop_words
-  replace_emojis
-  replace_hyphens
-  replace_punctuation
-  replace_symbols
-  replace_urls

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
-  Portuguese (pt)
-  Russian (ru)
-  Spanish (es)
-  Swedish (sv)
