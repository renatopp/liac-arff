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


Loading An Object with encoded labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases it is practical to have categorical data represented by
integers, rather than strings. In `scikit-learn <http://scikit-learn.org>`_ for
example, integer data can be directly converted in a continuous
representation with the `One-Hot Encoder
<http://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features>`_,
which is necessary for most machine learning algorithms, e.g.
`Support Vector Machines <http://en.wikipedia.org/wiki/Support_vector_machine>`_.
The values ``[u'sunny', u'overcast', u'rainy']`` of the attribute
``u'outlook'`` would be represented by ``[0, 1, 2]``. This representation can
be directly used the  `One-Hot Encoder
<http://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features>`_.

Encoding categorical data while reading it from a file saves at least one
memory copy and can be invoked like in this example::

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
    decoder = arff.ArffDecoder()
    d = decoder.decode(file_, encode_nominal=True)
    pprint.pprint(d)

resulting in::

    {u'attributes': [(u'outlook', [u'sunny', u'overcast', u'rainy']),
                 (u'temperature', u'REAL'),
                 (u'humidity', u'REAL'),
                 (u'windy', [u'TRUE', u'FALSE']),
                 (u'play', [u'yes', u'no'])],
     u'data': [[0, 85.0, 85.0, 1, 1],
               [0, 80.0, 90.0, 0, 1],
               [1, 83.0, 86.0, 1, 0],
               [2, 70.0, 96.0, 1, 0],
               [2, 68.0, 80.0, 1, 0],
               [2, 65.0, 70.0, 0, 1],
               [1, 64.0, 65.0, 0, 0],
               [0, 72.0, 95.0, 1, 1],
               [0, 69.0, 70.0, 1, 0],
               [2, 75.0, 80.0, 1, 0],
               [0, 75.0, 70.0, 0, 0],
               [1, 72.0, 90.0, 0, 0],
               [1, 81.0, 75.0, 1, 0],
               [2, 71.0, 91.0, 0, 1]],
     u'description': u'',
     u'relation': u'weather'}


Using this dataset in `scikit-learn <scikit-learn.org>`_::

    from sklearn import preprocessing, svm
    enc = preprocessing.OneHotEncoder(categorical_features=[0, 3, 4])
    enc.fit(d['data'])
    encoded_data = enc.transform(d['data']).toarray()
    clf = svm.SVC()
    clf.fit(encoded_data[:,0:4], encoded_data[:,4])


