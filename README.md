# normalizr

Normalizr is a Python library for text normalization that offers a bunch of actions to manipulate your text as much as you want. With normalizr you can replace symbols, punctuation, remove stop words and much more.


## Installation

The easiest way to install the latest version is by using pip to pull it from [PyPI](https://pypi.python.org/pypi/normalizr):

```
$ pip install normalizr
```

You may also use Git to clone the repository from Github and install it manually:

```
$ git clone https://github.com/davidmogar/normalizr.git
$ cd normalizr
$ python setup.py install
```

## Usage

The next code shows a sample usage of this library:

```python
from normalizr import Normalizr

normalizr = Normalizr(language='en')
print(normalizr.normalize('Who let the dog out?'))
```

        Note: Unicode strings are required. In case of using a Python version prior to 3.0, append a ``u`` before the text.
        
This would apply all normalizations to the text `Who let the dog out?`. The output for this normaliations would be the next one:

```
let dog
```

It's also possible to send a list of normalizations to apply, which will be executed in order.

```python
from normalizr import Normalizr

normalizr = Normalizr(language='en')

normalizations = [
    'remove_extra_whitespaces',
    ('replace_punctuation', {'replacement': ' '})
]

print(normalizr.normalize('Who    let   the dog out?', normalizations))
```

Output:

```
Who let the dog out
```

If you only need to apply one normalization, use one of these methods:

- remove_accent_marks
- remove_extra_whitespaces
- remove_stop_words
- replace_charachters
- replace_emails
- replace_emojis
- replace_hyphens
- replace_punctuation
- replace_symbols
- replace_urls

## Supported languages

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

## Contributing

So you have a new feature you think would be great for normalizr? Go for it! Pull request are warmly welcome.
Not in the mood of implement it yourself? You can still create an issue and tell about it there. Feedback is always great!
