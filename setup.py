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
    version = '0.0.15',
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
        '': [
            'contracts/etherdelta.json',
            'contracts/token.json'
        ],
    },
    dependency_links=[
        'git+ssh://github.com/ethereum/web3.py.git#egg=web3-4.0.0-beta.9'
    ],
    install_requires=[
        'web3==4.0.0-beta.9',
        'socketIO-client-2==0.7.5',
        'ethereum_utils==0.6.2',
        'eth_utils==1.0.0b1',
        'websocket_client==0.46.0'
    ]
)
