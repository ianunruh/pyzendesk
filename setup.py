#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pyzendesk',
    version='0.0.1',
    author='Ian Unruh',
    author_email='ianunruh@gmail.com',
    url='https://github.com/ianunruh/pyzendesk',
    packages=find_packages(),
    install_requires=[
        'requests',
        'six',
    ],
)
