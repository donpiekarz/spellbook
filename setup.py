#!/usr/bin/env python

import os

from setuptools import setup

from spellbooker import VERSION

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), 'rU') as f:
    long_description = f.read()

required = [
    'future'
]

extras = {
    'with_dropbox': ['dropbox>=4.0.0']
}

setup(
    name='spellbook',
    version=VERSION,
    packages=['spellbooker'],
    url='https://github.com/donpiekarz/spellbook',
    download_url='https://github.com/donpiekarz/spellbook/tarball/' + VERSION,
    license='BSD',
    author='Bartlomiej Piekarski',
    author_email='bartlomiej.piekarski@gmail.com',
    description='store and search command lines',
    long_description=long_description,
    entry_points={
        'console_scripts': ['spellbook = spellbooker.application:main']
    },
    install_requires=required,
    extras_require=extras,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: System :: Shells',
        'Topic :: System :: System Shells',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
