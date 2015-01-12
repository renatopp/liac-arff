What's New on LIAC-ARFF
=======================

LIAC-ARFF 2.0.2 (DEV)
---------------------

- fix: attribute names now must start with alphabetic character.
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
