==============
Forex, by Valuehorizon
==============

.. image:: https://travis-ci.org/Valuehorizon/valuehorizon-forex.svg?branch=master
   :target: https://travis-ci.org/Valuehorizon/valuehorizon-forex
.. image:: https://coveralls.io/repos/Valuehorizon/valuehorizon-forex/badge.svg
   :target: https://coveralls.io/r/Valuehorizon/valuehorizon-forex
.. image:: https://codeclimate.com/github/Valuehorizon/valuehorizon-forex/badges/gpa.svg
   :target: https://codeclimate.com/github/Valuehorizon/valuehorizon-forex

A Django-based Foreign Exchange data toolkit. It provides time-series functionality
with built-in statistical plugins such as volatility and returns. You can also write 
your own statistical plugins.
It also includes documentation, test coverage and a good amount of sample data to play around with.
This app is a part of the Valuehorizon application ecosystem.

Contributors
============
* `Kevin Ali <https://github.com/kevinali1>`_
* `Quincy Alexander <https://github.com/quincya>`_

Dependencies
=============
``forex`` supports `Django`_ (>=1.8.1) or later and requires and `Pandas`_ (>= 0.12.0). 
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

Next install ``numpy`` and ``pandas`` ::

    pip install numpy
    pip install pandas

Finally, install the development version of ``forex`` from ``github`` using ``pip``::
    
    pip install https://github.com/Valuehorizon/forex/tarball/master


Commercial Support
==================

This project is sponsored by Valuehorizon_. If you require assistance on
your project(s), please contact us: support@valuehorizon.com.

.. _Valuehorizon: http://www.valuehorizon.com