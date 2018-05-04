#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path

pwd = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(pwd, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'etherdelta',
    packages = ['etherdelta'],
    version = '0.0.22',
    url = 'https://github.com/coincircle/py-etherdelta',
    download_url = 'https://github.com/coincircle/py-etherdelta/archive/master.zip',
    author = 'Miguel Mota',
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
        'git+ssh://github.com/ethereum/web3.py.git@307dc87#egg=web3-4.0.0-beta.11'
    ],
    install_requires=[
        'web3==4.0.0-beta.11',
        'eth_utils==1.0.1',
        'websocket_client==0.46.0'
    ]
)
