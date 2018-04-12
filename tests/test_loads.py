import unittest
import arff
import datetime
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


ARFF = '''% XOR Dataset
@RELATION XOR

@ATTRIBUTE input1 REAL
@ATTRIBUTE input2 REAL
@ATTRIBUTE y REAL

@DATA
0.0,0.0,0.0
0.0,1.0,1.0
1.0,0.0,1.0
1.0,1.0,0.0
% 
% 
% '''

ARFF_FORMAT_CORRECT = '''\
@relation "software metric"

@attribute number_of_files numeric
@attribute "lines of code" numeric
@attribute 'defect density' numeric

@data 10,10,10
'''

SPARSE_ARFF = '''% XOR Dataset
@RELATION XOR

@ATTRIBUTE input1 REAL
@ATTRIBUTE input2 REAL
@ATTRIBUTE y REAL

@DATA
{0 0}
{1 1.0, 2 1.0}
{0 1.0, 2 1.0}
{0 1.0, 1 1.0}
'''


class TestLoads(unittest.TestCase):
    def get_loads(self):
        load = arff.loads
        return load

    def test_simple(self):
        loads = self.get_loads()
        obj = loads(ARFF)

        self.assertEqual(obj['description'], u'XOR Dataset')
        self.assertEqual(obj['relation'], u'XOR')
        self.assertEqual(obj['attributes'][0][0], u'input1')
        self.assertEqual(obj['attributes'][0][1], u'REAL')
        self.assertEqual(obj['data'][0][0], 0.0)
        self.assertEqual(obj['data'][0][1], 0.0)
        self.assertEqual(obj['data'][0][2], 0.0)

    def test_format_correct(self):
        loads = self.get_loads()
        obj = loads(ARFF_FORMAT_CORRECT)

        self.assertEqual(obj['attributes'][0][0], u'number_of_files')
        self.assertEqual(obj['attributes'][1][0], u'lines of code')
        self.assertEqual(obj['attributes'][2][0], u'defect density')

        self.assertEqual(obj['relation'], u'software metric')

    def test_format_error_relation(self):
        fixture = '''\
        @relation software metric

        @attribute number_of_files numeric
        @attribute "lines of code" numeric
        @attribute 'defect density' numeric

        @data 10,10,10
        '''
        loads = self.get_loads()
        fixture = u'@ATTRIBUTE {name NUMERIC'
        self.assertRaises(arff.BadLayout, loads, fixture)

    def test_format_error_attribute(self):
        fixture = '''\
        @relation "software metric"

        @attribute #_of_files numeric
        @attribute lines of code numeric
        @attribute defect density numeric

        @data 10,10,10
        '''

        loads = self.get_loads()
        fixture = u'@ATTRIBUTE {name NUMERIC'
        self.assertRaises(arff.BadLayout, loads, fixture)

    def test_sparse_input(self):
        loads = self.get_loads()
        obj = loads(ARFF)
        sparse_obj = loads(SPARSE_ARFF)
        self.assertEqual(obj['data'], sparse_obj['data'])

    def test_quoted_null(self):
        ARFF_WITH_NULL = '''% XOR Dataset
@RELATION XOR

@attribute 'bc' {'?','Y'}

@DATA
'Y'
'?'
'Y'
'?'
%
%
% '''

        loads = self.get_loads()
        obj = loads(ARFF_WITH_NULL)
        self.assertEqual(obj['data'], [['Y'], ['?'], ['Y'], ['?']])

    def test_date(self):
        '''Test the date conversion; by coercion.'''
        ARFF_WITH_DATE = '''% XOR Dataset
@RELATION event_date

@attribute occurs DATE

@DATA
'2011-01-11'
'2010-10-01'
%
%
% '''

        loads = self.get_loads()
        obj = loads(ARFF_WITH_DATE)
        self.assertEqual(obj['data'], [
            [datetime.datetime(2011, 1, 11, 0, 0)], [datetime.datetime(2010, 10, 1, 0, 0)]])


    def test_date_formatting(self):
        '''Test the date conversion using a supplied formatting string.'''
        ARFF_WITH_DATE = '''% XOR Dataset
@RELATION event_date

@attribute occurs DATE "%m/%d/%Y"

@DATA
"07/27/2012"
%
%
% '''

        loads = self.get_loads()
        obj = loads(ARFF_WITH_DATE)
        self.assertEqual(obj['data'], [[datetime.datetime(2012, 7, 27, 0, 0)]])

    def test_date_formatting_complex(self):
        '''Test the date conversion using a supplied complex formatting string.'''
        ARFF_WITH_DATE = '''% XOR Dataset
@RELATION event_date

@attribute occurs DATE "%m/%d/%Y HH:mm"

@DATA
"07/27/2012 12:34"
%
%
% '''

        loads = self.get_loads()
        obj = loads(ARFF_WITH_DATE)
        self.assertEqual(obj['data'], [[datetime.datetime(2012, 7, 27, 12, 34)]])
