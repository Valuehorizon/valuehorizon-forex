=======================
Forex, by Valuehorizon
=======================

.. image:: https://badge.fury.io/py/valuehorizon-forex.svg
   :target: http://badge.fury.io/py/valuehorizon-forex
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

Installation
============

Start by creating a new ``virtualenv`` for your project ::

    mkvirtualenv myproject

Next install ``numpy`` and ``pandas`` and optionally ``scipy`` ::

    pip install numpy==1.1.0
    pip install pandas==0.13.0

Finally, install ``valuehorizon-forex`` using ``pip``::

    pip install valuehorizon-forex

Usage
============

Let's start by loading some sample data.::

    python manage.py load_fixtures --settings=my_settings_file

This dataset contains the exchange rate data for the US Dollar to Euro (USD/EUR) from 2013-01-01 to 2015-12-31. In a 
django shell, we can try the following::

    euro = Currency.objects.get(symbol="EUR")


Contributing
============

Please file bugs and send pull requests to the `GitHub repository`_ and `issue
tracker`_.

.. _GitHub repository: https://github.com/Valuehorizon/valuehorizon-forex/
.. _issue tracker: https://github.com/Valuehorizon/valuehorizon-forex/issues

Commercial Support
==================

This project is sponsored by Valuehorizon_. If you require assistance on
your project(s), please contact us: support@valuehorizon.com.

.. _Valuehorizon: http://www.valuehorizon.com
