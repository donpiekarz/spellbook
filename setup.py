#!/usr/bin/env python

from distutils.core import setup

from spellbooker.application import VERSION

setup(
        name='spellbook',
        version=VERSION,
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
