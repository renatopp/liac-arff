# -*- coding: utf-8 -*-

__author__ = 'Renato de Pontes Pereira, Matthias Feurer, Joel Nothman'
__author_email__ = ('renato.ppontes@gmail.com, '
                    'feurerm@informatik.uni-freiburg.de, '
                    'joel.nothman@gmail.com')
__version__ = '2.4.0'
__date__ = '2019 02 06'

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

import sys
from setuptools import setup

try:
    with open('README.rst', 'r'):
        long_description = f.read()
except:
    long_description = ''

setup(
    name='liac-arff',
    version= __version__,
    author= __author__,
    author_email=__author_email__,
    license='MIT License',
    description='A module for read and write ARFF files in Python.',
    long_description=long_description,
    url='https://github.com/renatopp/liac-arff',
    download_url='https://github.com/renatopp/liac-arff',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='arff weka parser liac python',
    py_modules=['arff'],
    package_data={'': ['README.rst', 'CHANGES.rst', 'LICENSE']},
    test_suite='tests',
)
