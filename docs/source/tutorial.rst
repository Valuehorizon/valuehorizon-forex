Tutorial
=========

Simple instructions for installation and basic uses of the application. 


Install Forex
--------------------------

Start by creating a new virtualenv for your project::

   $ mkvirtualenv myproject

Next install numpy and pandas and optionally scipy::

   $ pip install numpy==1.8.0
   $ pip install scipy==0.13.3
   $ pip install pandas==0.13.0

Finally, install Valuehorizon Forex, either from a distribution package or from
`PyPI <https://pypi.python.org/pypi/valuehorizon-forex>`_ with ::

   $ pip install valuehorizon-forex


Usage
------

>>> from forex.models import *
>>> all=Currency.objects.all()











