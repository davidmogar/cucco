cucco |Build Status| |codecov|
==============================

Is that... is that a cucco? Sure it is!

Cucco is here to help you to normalize those nasty texts. Removing extra
whitespaces is not that hard, right? What about stop words? They make no
good... oh, and don't even mention emojis!

This little friend will do the hard work for you. Just set it up and let
him peck all over your text.

Oh please, shut up and show me where can I grab a cucco!
--------------------------------------------------------

The easiest way to get a cucco is by using pip:

::

    $ pip install cucco

But sometimes... sometimes you want to go wild and get the biggest...
No, the best!... No, THE MIGHTY cucco!

To do so, you may use Git. Clone the repository from Github and do it
all the hard way:

::

    $ git clone https://github.com/davidmogar/cucco.git
    $ cd cucco
    $ python setup.py install

Got it. How do I use it?
------------------------

Now that you have a cucco, I'll let him give you all the details.

    Cucuco, cuco cuco cucucuco, CUCCO!

    -- Cucco

So true... so true...[tears falling down my face]. Just allow me to add
some details.

The next example code shows how to normalize a short text:

.. code:: python

    from cucco import Cucco

    cucco = Cucco(language='en')
    print(cucco.normalize('Who let the cucco out?'))

This would apply all normalizations to the text
``Who let the cucco out?``. The output for this normaliations would be
the next one:

::

    let cucco

It's also possible to send a list of normalizations to apply, which will
be executed in order.

.. code:: python

    from cucco import Cucco

    cucco = Cucco(language='en')

    normalizations = [
        'remove_extra_whitespaces',
        ('replace_punctuation', {'replacement': ' '})
    ]

    print(cucco.normalize('Who    let   the cucco out?', normalizations))

This is the output:

::

    Who let the cucco out

Finally, if you only need to apply one normalization, use one of these
methods:

-  remove\_accent\_marks
-  remove\_extra\_whitespaces
-  remove\_stop\_words
-  replace\_charachters
-  replace\_emails
-  replace\_emojis
-  replace\_hyphens
-  replace\_punctuation
-  replace\_symbols
-  replace\_urls

Supported languages
-------------------

You never know when a cucco will learn a new trick but, at the moment,
they can remove stop words in these thirteen languages:

+------------+------------+-------------+------------+--------------+------------+
| Language   | Accronym   | Language    | Accronym   | Language     | Accronym   |
+============+============+=============+============+==============+============+
| Danish     | da         | German      | de         | Portuguese   | pt         |
+------------+------------+-------------+------------+--------------+------------+
| Dutch      | nl         | Hungarian   | hu         | Russian      | ru         |
+------------+------------+-------------+------------+--------------+------------+
| English    | en         | Italian     | it         | Spanish      | es         |
+------------+------------+-------------+------------+--------------+------------+
| Finnish    | fi         | Norwegian   | no         | Swedish      | sv         |
+------------+------------+-------------+------------+--------------+------------+
| French     | fr         |             |            |              |            |
+------------+------------+-------------+------------+--------------+------------+

Can I contribute?
-----------------

Are you a breeder? No? Don't worry, you can still help.

Maybe you have a good new feature to add. Maybe is not even good. It
doesn't matter! It is always good to share ideas, isn't it? Just go for
it! Pull request are warmly welcome.

Not in the mood of implement it yourself? You can still create an issue
and tell about it there. Feedback is always great!

.. |Build Status| image:: https://travis-ci.org/davidmogar/cucco.svg?branch=master
   :target: https://travis-ci.org/davidmogar/cucco
.. |codecov| image:: https://codecov.io/gh/davidmogar/cucco/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/davidmogar/cucco
