#!/usr/bin/python3
from setuptools import setup
setup(
    name='main.py',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'main=main:run'
        ]
    }
)
