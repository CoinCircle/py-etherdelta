#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from codecs import open  # To use a consistent encoding
from os import path

pwd = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(pwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'etherdelta',
    packages = ['etherdelta'],
    version = '0.0.7',
    url = 'https://github.com/miguelmota/py-etherdelta',
    download_url = 'https://github.com/miguelmota/py-etherdelta/archive/master.zip',
    author = 'Miguel Mota <hello@miguelmota.com>',
    author_email = 'hello@miguelmota.com',
    license = 'MIT License',
    description = 'Python wrapper for interacting with the EtherDelta API and Smart Contracts.',
    long_description = long_description,
    keywords = ['etherdelta'],
    include_package_data=True,
    package_data={
        'contracts': [
            'etherdelta.json',
            'token.json'
        ],
    },
)
