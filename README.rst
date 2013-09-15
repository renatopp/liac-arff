=========
liaf-arff
=========

The liac-arff module implements functions to read and write ARFF files in 
Python. 

Attribute Relationship File Format (`ARFF <http://weka.wikispaces.com/ARFF>`_) 
is the text format file used by Weka to store data in a database. This module 
is an ARFF file handler based on other python parser modules (such json and 
yaml).


NOTE: You can clone the `arff-datasets <https://github.com/renatopp/arff-datasets>`_ 
repository for a large set of ARFF files.


Features
--------

- Read and Write ARFF files using python built-in structures;
- Supports NUMERIC, REAL, INTEGER, STRING and NOMINAL attribute types;
- Supports names with space;
- Read and Write the description of the file;
- MIT license;


Install
-------

Via easy_install::

    $ easy_install liac-arff

Manually::

    $ python setup.py install


Usage
-----

You can read an ARFF file as follows::

    >>> import arff
    >>> data = arff.load(open('wheater.arff', 'rb'))

Which results in::

    >>> data
    {
    'attributes': [
        ('outlook', ['sunny', 'overcast', 'rainy']),
        ('temperature', 'REAL'),
        ('humidity', 'REAL'),
        ('windy', ['TRUE', 'FALSE']),
        ('play', ['yes', 'no'])],
    'data': [
        ['sunny', 85.0, 85.0, 'FALSE', 'no'],
        ['sunny', 80.0, 90.0, 'TRUE', 'no'],
        ['overcast', 83.0, 86.0, 'FALSE', 'yes'],
        ['rainy', 70.0, 96.0, 'FALSE', 'yes'],
        ['rainy', 68.0, 80.0, 'FALSE', 'yes'],
        ['rainy', 65.0, 70.0, 'TRUE', 'no'],
        ['overcast', 64.0, 65.0, 'TRUE', 'yes'],
        ['sunny', 72.0, 95.0, 'FALSE', 'no'],
        ['sunny', 69.0, 70.0, 'FALSE', 'yes'],
        ['rainy', 75.0, 80.0, 'FALSE', 'yes'],
        ['sunny', 75.0, 70.0, 'TRUE', 'yes'],
        ['overcast', 72.0, 90.0, 'TRUE', 'yes'],
        ['overcast', 81.0, 75.0, 'FALSE', 'yes'],
        ['rainy', 71.0, 91.0, 'TRUE', 'no']],
    'description': u'',
    'relation': 'weather'
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


Project Page
------------

https://github.com/renatopp/liac-arff
