==============
LIAC-ARFF v2.1
==============

.. contents:: Table of Contents
   :depth: 2 
   :local:

------------
Introduction
------------

.. automodule:: arff

~~~~~~~~~~~~~~~~~~~~
How to Get LIAC-ARFF
~~~~~~~~~~~~~~~~~~~~

See https://github.com/renatopp/liac-arff

~~~~~~~~~~~~~~
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

LIAC-ARFF works with unicode (for python 2.7+, in python 3.x this is default),
and to take advantage of it, you need to load the arff file using ``codecs``,
specifying its codification::

    import codecs
    import arff

    file_ = codecs.open('/path/to/file.arff', 'rb', 'utf-8')
    arff.load(file_)


--------
Examples
--------

~~~~~~~~~~~~~~~~~
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


~~~~~~~~~~~~~~~~~
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


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Loading An Object with encoded labels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases it is practical to have categorical data represented by
integers, rather than strings. In `scikit-learn <http://scikit-learn.org>`__ for
example, integer data can be directly converted in a continuous
representation with the `One-Hot Encoder
<http://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features>`__,
which is necessary for most machine learning algorithms, e.g.
`Support Vector Machines <http://en.wikipedia.org/wiki/Support_vector_machine>`__.
The values ``[u'sunny', u'overcast', u'rainy']`` of the attribute
``u'outlook'`` would be represented by ``[0, 1, 2]``. This representation can
be directly used the  `One-Hot Encoder
<http://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features>`__.

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


Using this dataset in `scikit-learn <scikit-learn.org>`__::

    from sklearn import preprocessing, svm
    enc = preprocessing.OneHotEncoder(categorical_features=[0, 3, 4])
    enc.fit(d['data'])
    encoded_data = enc.transform(d['data']).toarray()
    clf = svm.SVC()
    clf.fit(encoded_data[:,0:4], encoded_data[:,4])

.. _sparse:

~~~~~~~~~~~~~~~~~~~~~~~~
Working with sparse data
~~~~~~~~~~~~~~~~~~~~~~~~

Sparse data is data in which most of the elements are zero. By saving only
non-zero elements, one can potentially save a lot of space on either the
harddrive or in RAM. liac-arff supports two sparse data structures:

* `scipy.sparse.coo <http://docs.scipy.org/doc/scipy/reference/sparse.html>`__
  is intended for easy construction of sparse matrices inside a python program.
* list of dictionaries in the form

  .. code:: python

      [{column: value, column: value},
       {column: value, column: value}]


Dumping sparse data
~~~~~~~~~~~~~~~~~~~

Both `scipy.sparse.coo <http://docs.scipy.org/doc/scipy/reference/sparse.html>`__
matrices and lists of dictionaries can be used as the value for `data` in the
arff object. Let's look again at the XOR example, this time with the data
encoded as a list of dictionaries:

.. code:: python

    xor_dataset = {
        'description': 'XOR Dataset',
        'relation': 'XOR',
        'attributes': [
            ('input1', 'REAL'),
            ('input2', 'REAL'),
            ('y', 'REAL'),
        ],
        'data': [
            {},
            {1: 1.0, 2: 1.0},
            {0: 1.0, 2: 1.0},
            {0: 1.0, 1: 1.0}
        ]
    }

    print arff.dumps(xor_dataset)

resulting in::

    % XOR Dataset
    @RELATION XOR

    @ATTRIBUTE input1 REAL
    @ATTRIBUTE input2 REAL
    @ATTRIBUTE y REAL

    @DATA
    {  }
    { 1 1.0,2 1.0 }
    { 0 1.0,2 1.0 }
    { 0 1.0,1 1.0 }
    %
    %
    %

Loading sparse data
~~~~~~~~~~~~~~~~~~~

When reading a sparse dataset, the user can choose a target data structure.
These are represented by the constants `arff.DENSE`, `arff.COO` and `arff.LOD`::

    decoder = arff.ArffDecoder()
    d = decoder.decode(file_, encode_nominal=True, return_type=arff.LOD)
    pprint.pprint(d)

resulting in::

    {
        'description': 'XOR Dataset',
        'relation': 'XOR',
        'attributes': [
            ('input1', 'REAL'),
            ('input2', 'REAL'),
            ('y', 'REAL'),
        ],
        'data': [
            {},
            {1: 1.0, 2: 1.0},
            {0: 1.0, 2: 1.0},
            {0: 1.0, 1: 1.0}
        ]
    }

When choosing `arff.COO`, the data can be dircetly passed to the scipy
constructor::

    from scipy import sparse
    decoder = arff.ArffDecoder()
    d = decoder.decode(file_, encode_nominal=True, return_type=arff.COO)
    data = d['data'][0]
    row = d['data'][1]
    col = d['data'][2]
    matrix = sparse.coo_matrix((data, (row, col)), shape=(max(row)+1, max(col)+1))


Working with Date objects
~~~~~~~~~~~~~~~~~~~~~~~~~

Date data can be encoded into an arff file as an attribute and an optional format
specification can be made.
The recommended format is: ISO 8601 format, YYYY-MM-DDTHH:MM:SS.mmmmmm; however,
any level of precision is acceptable. The format string must contain the proper
percent sign escaped formatting characters, e.g.: '%Y/%m/%dT%H:%M:%S'. Because date
values may contain a space, their data representations should be quoted.

If no format specification is given, the date format will be guessed using the
dateutil library; the closer the data is in the format of ISO 8601, the greater the
chance of a successful conversion.
Serializing an arff data structure will use the ISO 8601 formatting.

Here is an example::

   import arff
   import pprint

   file_ = '''@RELATION employee
   @ATTRIBUTE Name STRING
   @ATTRIBUTE start_date DATE
   @ATTRIBUTE end_date DATE '%Y/%m/%dT%H:%M:%S'
   @ATTRIBUTE simple_date DATE '%Y/%m/%d'
   @DATA
   Lulu,'2011-05-20T12:34:56','2014/06/21T12:34:56','2018/03/04'
   Daisy,'2012-09-30T12:34:56','2015/11/21T12:34:56','2018/03/04'
   Brie,'2013-05-01T12:34:56','2016/12/21T12:34:56','2018/03/04'
   '''
   decoder = arff.ArffDecoder()
   d = decoder.decode(file_, encode_nominal=True)
   pprint.pprint(d)

resulting in::

   {'attributes': [('Name', 'STRING'),
                    ('start_date', 'DATE'),
                    ('end_date', 'DATE', "'%Y/%m/%dT%H:%M:%S'"),
                    ('simple_date', 'DATE', "'%Y/%m/%d'")],
    'data': [['Lulu',
               datetime.datetime(2011, 5, 20, 12, 34, 56),
               datetime.datetime(2014, 6, 21, 12, 34, 56),
               datetime.datetime(2018, 3, 4, 0, 0)],
              ['Daisy',
               datetime.datetime(2012, 9, 30, 12, 34, 56),
               datetime.datetime(2015, 11, 21, 12, 34, 56),
               datetime.datetime(2018, 3, 4, 0, 0)],
              ['Brie',
               datetime.datetime(2013, 5, 1, 12, 34, 56),
               datetime.datetime(2016, 12, 21, 12, 34, 56),
               datetime.datetime(2018, 3, 4, 0, 0)]],
    'description': '',
    'relation': 'employee'}
