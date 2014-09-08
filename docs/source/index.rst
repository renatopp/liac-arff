==============
LIAC-ARFF v2.0
==============

.. contents:: Table of Contents
   :depth: 2 
   :local:

------------
Introduction
------------

.. automodule:: arff


How to Get LIAC-ARFF
~~~~~~~~~~~~~~~~~~~~

See https://github.com/renatopp/liac-arff


How To Install
~~~~~~~~~~~~~~

Via pip::

    $ pip install liac-arff

Via easy_install::

    $ easy_install liac-arff

Manually::

    $ python setup.py install


-----------
Basic Usage
-----------

.. autofunction:: arff.load
.. autofunction:: arff.loads
.. autofunction:: arff.dump
.. autofunction:: arff.dumps


---------------------
Encoders and Decoders
---------------------

.. autoclass:: arff.ArffDecoder
   :members:

.. autoclass:: arff.ArffEncoder
   :members:


----------
Exceptions
----------

.. autoexception:: arff.BadRelationFormat
   :members:

.. autoexception:: arff.BadAttributeFormat
   :members:

.. autoexception:: arff.BadDataFormat
   :members:

.. autoexception:: arff.BadAttributeType
   :members:

.. autoexception:: arff.BadNominalValue
   :members:

.. autoexception:: arff.BadNumericalValue
   :members:

.. autoexception:: arff.BadLayout
   :members:

.. autoexception:: arff.BadObject
   :members:


-------
Unicode
-------

LIAC-ARFF works with unicode (for python 2.6+, in python 3.x this is default),
and to take advantage of it, you need to load the arff file using ``codecs``,
specifying its codification::

    import codecs
    import arff

    file_ = codecs.load('/path/to/file.arff', 'rb', 'utf-8')
    arff.load(file_)


--------
Examples
--------

Dumping An Object
~~~~~~~~~~~~~~~~~

Converting an object to ARFF::

    import arff

    obj = {
       'description': u'',
       'relation': 'weather',
       'attributes': [
           ('outlook', ['sunny', 'overcast', 'rainy']),
           ('temperature', 'REAL'),
           ('humidity', 'REAL'),
           ('windy', ['TRUE', 'FALSE']),
           ('play', ['yes', 'no'])
       ],
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
           ['rainy', 71.0, 91.0, 'TRUE', 'no']
       ],
    }

   print arff.dumps(obj)

resulting in::

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


Loading An Object
~~~~~~~~~~~~~~~~~

Loading and ARFF file::

    import arff
    import pprint

    file_ = '''@RELATION weather

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
    % '''
    d = arff.loads(file_)
    pprint.pprint(d)

resulting in::

    {u'attributes': [(u'outlook', [u'sunny', u'overcast', u'rainy']),
                     (u'temperature', u'REAL'),
                     (u'humidity', u'REAL'),
                     (u'windy', [u'TRUE', u'FALSE']),
                     (u'play', [u'yes', u'no'])],
     u'data': [[u'sunny', 85.0, 85.0, u'FALSE', u'no'],
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
               [u'rainy', 71.0, 91.0, u'TRUE', u'no']],
     u'description': u'',
     u'relation': u'weather'}