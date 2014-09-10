=========
LIAC-ARFF
=========

The liac-arff module implements functions to read and write ARFF files in
Python. It was created in the Connectionist Artificial Intelligence Laboratory
(LIAC), which takes place at the Federal University of Rio Grande do Sul 
(UFRGS), in Brazil.

ARFF (Attribute-Relation File Format) is an file format specially created for
describe datasets which are used commonly for machine learning experiments and
softwares. This file format was created to be used in Weka, the best 
representative software for machine learning automated experiments.

You can clone the `arff-datasets <https://github.com/renatopp/arff-datasets>`_ 
repository for a large set of ARFF files.

--------
Features
--------

- Read and write ARFF files using python built-in structures, such dictionaries
  and lists;
- Supports the following attribute types: NUMERIC, REAL, INTEGER, STRING, and
  NOMINAL;
- Has an interface similar to other built-in modules such as ``json``, or 
  ``zipfile``;
- Supports read and write the descriptions of files;
- Supports missing values and names with spaces;
- Supports unicode values and names;
- Fully compatible with Python 2.6+ and Python 3.4+;
- Under `MIT License <http://opensource.org/licenses/MIT>`_

--------------
How To Install
--------------

Via pip::

    $ pip install liac-arff

Via easy_install::

    $ easy_install liac-arff

Manually::

    $ python setup.py install


-------------
Documentation
-------------

For a complete description of the module, consult the official documentation at
http://packages.python.org/liac-arff/ with mirror in
http://inf.ufrgs.br/~rppereira/arff/index.html


-----
Usage
-----

You can read an ARFF file as follows::

    >>> import arff
    >>> data = arff.load(open('wheater.arff', 'rb'))

Which results in::

    >>> data
    {
        u'attributes': [
            (u'outlook', [u'sunny', u'overcast', u'rainy']),
            (u'temperature', u'REAL'),
            (u'humidity', u'REAL'),
            (u'windy', [u'TRUE', u'FALSE']),
            (u'play', [u'yes', u'no'])],
        u'data': [
            [u'sunny', 85.0, 85.0, u'FALSE', u'no'],
            [u'sunny', 80.0, 90.0, u'TRUE', u'no'],
            [u'overcast', 83.0, 86.0, u'FALSE', u'yes'],
            [u'rainy', 70.0, 96.0, u'FALSE', u'yes'],
            [u'rainy', 68.0, 80.0, u'FALSE', u'yes'],
            [u'rainy', 65.0, 70.0, u'TRUE', u'no'],
            [u'overcast', 64.0, 65.0, u'TRUE', u'yes'],
            [u'sunny', 72.0, 95.0, u'FALSE', u'no'],
            [u'sunny', 69.0, 70.0, u'FALSE', u'yes'],
            [u'rainy', 75.0, 80.0, u'FALSE', u'yes'],
            [u'sunny', 75.0, 70.0, u'TRUE', u'yes'],
            [u'overcast', 72.0, 90.0, u'TRUE', u'yes'],
            [u'overcast', 81.0, 75.0, u'FALSE', u'yes'],
            [u'rainy', 71.0, 91.0, u'TRUE', u'no']
        ],
        u'description': u'',
        u'relation': u'weather'
    }

You can write an ARFF file with this structure::

    >>> print arff.dumps(data)
    @RELATION weather

    @ATTRIBUTE outlook {sunny, overcast, rainy}
    @ATTRIBUTE temperature REAL
    @ATTRIBUTE humidity REAL
    @ATTRIBUTE windy {TRUE, FALSE}
    @ATTRIBUTE play {yes, no}

    @DATA
    sunny,85.0,85.0,FALSE,no
    sunny,80.0,90.0,TRUE,no
    overcast,83.0,86.0,FALSE,yes
    rainy,70.0,96.0,FALSE,yes
    rainy,68.0,80.0,FALSE,yes
    rainy,65.0,70.0,TRUE,no
    overcast,64.0,65.0,TRUE,yes
    sunny,72.0,95.0,FALSE,no
    sunny,69.0,70.0,FALSE,yes
    rainy,75.0,80.0,FALSE,yes
    sunny,75.0,70.0,TRUE,yes
    overcast,72.0,90.0,TRUE,yes
    overcast,81.0,75.0,FALSE,yes
    rainy,71.0,91.0,TRUE,no
    %
    %
    %


Contributors
------------

- `Nate Moseley (FinalDoom) <https://github.com/FinalDoom>`_
- `Tarek Amr (gr33ndata) <https://github.com/gr33ndata>`_
- `Simon (M3t0r) <https://github.com/M3t0r>`_
- `Gonzalo Almeida (flecox) <https://github.com/flecox>`_
- `André Nordbø (AndyNor) <http://andynor.net>`_
- `Niedakh <https://github.com/niedakh>`_
- `Zichen Wang (wangz10) <https://github.com/wangz10>`_
- `Matthias Feurer (mfeurer) <https://github.com/mfeurer>`_
- `Hongjoo Lee (midnightradio) <https://github.com/midnightradio>`_

Project Page
------------

https://github.com/renatopp/liac-arff
