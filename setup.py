#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'etherdelta',
    packages = ['etherdelta'],
    version = '0.0.1',
    url = 'https://github.com/miguelmota/py-etherdelta',
    download_url = 'https://github.com/miguelmota/py-etherdelta/archive/master.zip',
    author = 'Miguel Mota <hello@miguelmota.com>',
    author_email = 'hello@miguelmota.com',
    license = 'MIT License',
    description = 'Python wrapper for interacting with the EtherDelta API and Smart Contracts.',
    long_description = open('README.md','r').read(),
    keywords = ['etherdelta'],
)
