# -*- encoding: utf-8 -*-
"""
Python setup file for the forex app.

"""
import os
from setuptools import setup, find_packages
import forex as app


dev_requires = [
    'flake8',
]

install_requires = [
    # User should install requirements
]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="valuehorizon-forex",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, app, reusable, finance, forex, foreign exchange, valuehorizon',
    author='Quincy Alexander',
    author_email='qalexander@valuehorizon.com',
    url="https://github.com/Valuehorizon/valuehorizon-forex",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
    test_suite="forex.tests.runtests.runtests"
)
