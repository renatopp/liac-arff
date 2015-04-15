====================
rustle1314/liac-arff
====================

I have modified some code to make liac-arff to handle large-scale data.

The main changes are two, namely 1) adding the ArffDecoder and 2) chaning 
the ArffEncoder.iter_encode method. These changes will not change the 
usages of the original interfaces (i.e., the four methods: load, loads, 
dump, dumps).

1. Adding the ArffDecoder.iter_decode method.
--------------------------------------------

1.1 params

ArffDecoder.iter_decode(self, file, encode_nominal = False, obj = None,
batch = 20). The params are listed as follows::
  
- file, the arff file to read and decode.
- encode_nominal, I don't what the param is for. 囧. (default false). 
- obj,  python representation of a given ARFF file (default None).
- batch,  the number of instances once (default 20).
  
1.2 usages and examples
  
You are expected to set the param obj = None when you first call the method. 
At the first call, the iter_decode will read the arff file and decode the Arff 
information (i.e., relations, attributes...) and some instances. 
  
The param obj are expected to be set as the return of the previous call at the 
subsequent calls. At this time, the iter_decode will update the instances in obj 
with the arff file.

Here is an example. Assume the content in the test.arff::
      
      @RELATION weather\n
      \n
      @ATTRIBUTE outlook {sunny, overcast, rainy}\n
      @ATTRIBUTE temperature REAL\n
      @ATTRIBUTE humidity REAL\n
      @ATTRIBUTE windy {TRUE, FALSE}\n
      @ATTRIBUTE play {yes, no}\n
      \n
      @DATA\n
      sunny,85.0,85.0,FALSE,no\n
      sunny,80.0,90.0,TRUE,no\n
      overcast,83.0,86.0,FALSE,yes\n

There are two instances in the arff file. Then We run the code::
  
      >>> f = open("test.arff");
      >>> decoder = ArffDecoder();
      >>> obj1    = decoder.iter_decode(f, obj = None, batch = 2);
      >>> obj2    = decoder.iter_decode(f, obj = obj1, batch = 2);
  
  
The results are::
  
      >>> obj1
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
          ],
          u'description': u'',
          u'relation': u'weather'
      }
      >>> obj2
      {
          u'attributes': [
            (u'outlook', [u'sunny', u'overcast', u'rainy']),
            (u'temperature', u'REAL'),
            (u'humidity', u'REAL'),
            (u'windy', [u'TRUE', u'FALSE']),
            (u'play', [u'yes', u'no'])],
          u'data': [
            [u'overcast', 83.0, 86.0, u'FALSE', u'yes'],
          ],
          u'description': u'',
          u'relation': u'weather'
      }
  
The obj1 contains the first two instances and the obj2 contains 
the last instance.
  
2. Chaning the ArffEncoder.iter_encode method.
---------------------------------------------
  
2.1 params

Definition of the method is ArffEncoder.iter_encode(obj, is_first_call =
True). The params are listed as follows::
  
- obj, the python representation of arff data.
- is_first_call, an indicator of the first call (default True).
  
2.2 usages and examples

When is_first_call = True, the modified ArffEncoder.iter_encode is identical
to the original one, which will encode the whole objection include the arff
information. 
  
When is_first_call = False, the method only encodes the data in the objection.
  
By using the modified method, you can write a part of  data into a file once
they are produced, instead of wait until all data are produced. It may be 
useful when the whole data are very large.
  
Here is an example of usage of this modified method.
  
      >>> obj 
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
        ],
          u'description': u'',
          u'relation': u'weather'
      }
  
If we set is_first_call = True::
  
      >>> encoder = ArffEncoder();
      >>> result = encoder.iter_encode(obj, is_first_call = True);
      >>> for i in result:
      ...     print i+u'\n',;
      ...
      @RELATION weather
      
      @ATTRIBUTE outlook {sunny, overcast, rainy}
      @ATTRIBUTE temperature REAL
      @ATTRIBUTE humidity REAL
      @ATTRIBUTE windy {TRUE, FALSE}
      @ATTRIBUTE play {yes, no}

      @DATA
      sunny,85.0,85.0,FALSE,no
      sunny,80.0,90.0,TRUE,no
      %
      %
      %
  
If we set is_first_call = False::   
  
      >>> encoder = ArffEncoder();
      >>> result = encoder.iter_encode(obj, is_first_call = False);
      >>> for i in result:
      ...     print i+u'\n',;
      ...
      sunny,85.0,85.0,FALSE,no
      sunny,80.0,90.0,TRUE,no
      %
      %
      %
  
      
      
  
Contributors
------------

- `lietal <https://github.com/rustle1314>`_




The original readme of liac-arff is as follows:
-----------------------------------------------

=========
LIAC-ARFF
=========

.. image:: https://travis-ci.org/renatopp/liac-arff.svg
    :target: https://travis-ci.org/renatopp/liac-arff

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
- Fully compatible with Python 2.6+ and Python 3.3+;
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
- `Calvin Jeong (calvin) <http://ty.pe.kr/>`_

Project Page
------------

https://github.com/renatopp/liac-arff
