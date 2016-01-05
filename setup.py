#!/usr/bin/env python

import setuptools

from distutils.core import setup

setup(
        name='spellbook',
        version='1.0.0',
        packages=['spellbooker'],
        url='https://github.com/donpiekarz/spellbook',
        license='BSD',
        author='Bartłomiej Piekarski',
        author_email='bartlomiej.piekarski@gmail.com',
        description='tool to easy search command lines',
        entry_points={
            'console_scripts': ['spellbook = spellbooker.application:main']
        }
)
