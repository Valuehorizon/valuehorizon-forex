==============
Forex, by Valuehorizon
==============

A Django-based Foreign Exchange data toolkit. Part of the Valuehorizon application ecosystem.

Contributors
============
* `Kevin Ali <https://github.com/kevinali1>`_
* `Quincy Alexander <https://github.com/quincya>`_

Dependencies
=============
``forex`` supports `Django`_ (>=1.7) or later and requires and `Pandas`_ (>= 0.12.0). 
**Note** because of problems with the ``requires`` directive of setuptools
you probably need to install ``numpy`` in your virtualenv  before you install
this package or if you want to run the test suite ::

    pip install numpy
    python setup.py test

Some ``pandas`` functionality requires parts of the Scipy stack.
You may wish to consult http://www.scipy.org/install.html 
for more information on installing the ``Scipy`` stack. 

.. _Django: http://djangoproject.com/
.. _Pandas: http://pandas.pydata.org

Contributing
============

Please file bugs and send pull requests to the `GitHub repository`_ and `issue
tracker`_.

.. _GitHub repository: https://github.com/Valuehorizon/forex/
.. _issue tracker: https://github.com/Valuehorizon/forex/issues


Installation
=============
Start by creating a new ``virtualenv`` for your project ::

    mkvirtualenv myproject

Next install ``numpy`` and ``pandas`` and optionally ``scipy`` ::

    pip install numpy
    pip install pandas

You may want to consult  the `scipy documentation`_ for more information 
on installing the ``Scipy`` stack.

.. _scipy documentation: http://www.scipy.org/install.html

Finally, install the development version of ``forex`` from ``github`` using ``pip``::
    
    pip install https://github.com/Valuehorizon/forex/tarball/master

