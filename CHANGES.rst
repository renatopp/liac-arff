What's New on LIAC-ARFF
=======================

LIAC-ARFF 2.2.3

- new: test for python3.7 and pypy3

LIAC-ARFF 2.2.2

- fix: better support for string and nominal features containing escape
  characters (issue #69).

LIAC-ARFF 2.2.1
---------------

- fix: better support for string features and nominals containing commas
  (issue # 64)

LIAC-ARFF 2.2
-------------

- fix: do not treat quoted questionmarks as missing values (issue #50)
- fix: compability issue using zip with python2.7
- fix: categorical quoting if comma is present (issue #15)
- fix: remove training comment lines (issue #61)
- new: test for python3.5 and python3.6 as well
- new: drop python2.6 support


LIAC-ARFF 2.1.1
---------------

- fix: working for 2.6+
- fix: working for 3.3+
- new: encoder checks if data has all attributes
- new: sparse data support


LIAC-ARFF 2.1.0
---------------

- fix: working for 2.6+
- fix: working for 3.3+
- new: encoder checks if data has all attributes
- new: sparse data support


LIAC-ARFF 2.0.2
---------------

- fix: attribute and relation names now follow the new ARFF specification.
- new: encoded nominal values.


LIAC-ARFF 2.0.1
---------------

- fix: dump now escapes correctly special symbols, such %, ', ", and \.


LIAC-ARFF 2.0
-------------

- new: ArffEncoder and ArffDecoder helpers which actually do the serialization
  and loading of ARFF files.
- new: UnitTest cases for all classes and functions.
- new: Detailed exceptions for many cases.
- fix: load, loads, dump, dumps are now simpler.
- rem: arfftools.py and the split function.


LIAC-ARFF 1.0
-------------

First commit.

- new: load, loads, dump, dumps functions
