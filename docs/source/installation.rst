Installation
=========

Simple instructions for installation and configuration of the Valuehorizon Forex application. 


Install Forex
--------------------------

Start by creating a new virtualenv for your project::

   $ mkvirtualenv myproject

Next install the Valuehorizon Forex application::
	
   $ pip install valuehorizon-forex

Finally, install Valuehorizon Forex, from the `PyPI <https://pypi.python.org/pypi/valuehorizon-forex>`_ distribution package with::

   $ pip install valuehorizon-forex

Dependencies
--------------------------

Valuehorizon Forex has a few dependencies that are requried for its time series functionality.
The following commands are for installing these dependencies on a Ubuntu Linux machine.

First, install the ``python-dev`` library through the package manager::

   $ sudo apt-get install python-dev

Next, install ``numpy`` and ``pandas``::
   
   $ pip install numpy
   $ pip install pandas

Optionally, you can install ``scipy`` to access some of the advanced features of pandas::
   
   $ pip install pandas

If you are trying to install on a Windows or Mac machine, then we recommend using the 
`Enthought Canopy <https://www.enthought.com/products/canopy/package-index>`_ package index.

Configuration
-------------

Add ``'forex'`` to the ``INSTALLED_APPS`` section in your django settings file.











