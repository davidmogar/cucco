cucco |Build Status| |codecov| |beerpay|
========================================

Is that... is that a cucco? Sure it is!

Cucco is here to help you to normalize those nasty texts. Removing extra whitespaces is not that hard, right? What about stop words? They're no good... oh, and don't even mention emojis!

This little friend will do the hard work for you. Just set it up and let it peck all over your text.

Oh please, shut up and show me where can I grab a cucco!
--------------------------------------------------------

The easiest way to get a cucco is by using pip:

::

    $ pip install cucco

But sometimes... sometimes you want to go wild and get the biggest... No, the best!... No, THE MIGHTIEST cucco!

To do so, you may use Git. Clone the repository from Github and do it all the hard way:

::

    $ git clone https://github.com/davidmogar/cucco.git
    $ cd cucco
    $ python setup.py install

Got it. How do I use it?
------------------------

Now that you have a cucco, I'll let it give you all the details.

    Cucuco, cuco cuco cucucuco, CUCCO!

    -- Cucco

So true... so true...[tears falling down my face]. Just allow me to add some insight.

There are two ways of using cucco. The first one is through its CLI. You can get more info on this by executing the next command:

::

    $ cucco --help

The next example code shows how to normalize a short text using cucco inside your code:

.. code:: python

    from cucco import Cucco

    cucco = Cucco()
    print(cucco.normalize('Who let the cucco out?'))

This would apply all normalizations to the text ``Who let the cucco out?``. The output for this normalizations would be the next one:

::

    cucco

It's also possible to send a list of normalizations to apply, which will be executed in order.

.. code:: python

    from cucco import Cucco

    cucco = Cucco()

    normalizations = [
        'remove_extra_whitespaces',
        ('replace_punctuation', {'replacement': ' '})
    ]

    print(cucco.normalize('Who    let   the cucco out?', normalizations))

This is the output:

::

    Who let the cucco out

For more information on how to use cucco you can `check its website <cucco.io>`_, which will be ready cucco-soon.

Supported languages
-------------------

You never know when a cucco will learn a new trick. Currently, they can remove stop words for 50 languages. The complete list can be `checked here <https://github.com/davidmogar/cucco/tree/master/cucco/data>`_. If you are looking for the source you can find it in this `GitHub repository <https://github.com/6/stopwords-json>`_ which uses `json` for the stop words files.

Can I contribute?
-----------------

Are you a breeder? No? Don't worry, you can still help.

Maybe you have a good new feature to add. Maybe is not even good. It doesn't matter! It is always good to share ideas, isn't it? Just go for it! Pull requests are warmly welcomed.

Not in the mood to implement it yourself? You can still create an issue and comment about it there. Feedback is always great!

.. |Build Status| image:: https://travis-ci.org/davidmogar/cucco.svg?branch=master
   :target: https://travis-ci.org/davidmogar/cucco
.. |codecov| image:: https://codecov.io/gh/davidmogar/cucco/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/davidmogar/cucco
.. |beerpay| image:: https://beerpay.io/davidmogar/cucco/badge.svg?style=flat
   :target: https://beerpay.io/davidmogar/cucco
