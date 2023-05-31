import unittest
import arff


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

        self.assertEqual(obj['description'], 'XOR Dataset')
        self.assertEqual(obj['relation'], 'XOR')
        self.assertEqual(obj['attributes'][0][0], 'input1')
        self.assertEqual(obj['attributes'][0][1], 'REAL')
        self.assertEqual(obj['data'][0][0], 0.0)
        self.assertEqual(obj['data'][0][1], 0.0)
        self.assertEqual(obj['data'][0][2], 0.0)

    def test_format_correct(self):
        loads = self.get_loads()
        obj = loads(ARFF_FORMAT_CORRECT)

        self.assertEqual(obj['attributes'][0][0], 'number_of_files')
        self.assertEqual(obj['attributes'][1][0], 'lines of code')
        self.assertEqual(obj['attributes'][2][0], 'defect density')

        self.assertEqual(obj['relation'], 'software metric')

    def test_format_error_relation(self):
        fixture = '''\
        @relation software metric

        @attribute number_of_files numeric
        @attribute "lines of code" numeric
        @attribute 'defect density' numeric

        @data 10,10,10
        '''
        loads = self.get_loads()
        fixture = '@ATTRIBUTE {name NUMERIC'
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
        fixture = '@ATTRIBUTE {name NUMERIC'
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
