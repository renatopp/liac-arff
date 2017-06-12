# -*- coding: utf-8 -*-

__author__ = 'Renato de Pontes Pereira, Matthias Feurer'
__author_email__ = 'renato.ppontes@gmail.com, feurerm@informatik.uni-freiburg.de'
__version__ = '2.1.1'
__date__ = '2017 06 12'

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

try:
    f = open('README.rst','rU')
    long_description = f.read()
    f.close()
except:
    long_description = ''

setup(
    name = 'liac-arff',
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    license='MIT License',
    description = 'A module for read and write ARFF files in Python.',
    long_description=long_description,
    url = 'https://github.com/renatopp/liac-arff',
    download_url = 'https://github.com/renatopp/liac-arff',
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
        ('Topic :: Software Development :: Libraries :: Python Modules'),
        ('Topic :: Scientific/Engineering :: Artificial Intelligence'),
    ],
    keywords='arff weka parser liac python',
    py_modules=['arff'],
    package_data={'':['README.rst', 'CHANGES.rst', 'LICENSE']},
    test_suite='tests',
)
