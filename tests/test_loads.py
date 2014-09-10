import unittest
import arff
import StringIO

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
        ARFF_FORMAT_ERROR_RELATION = '''\
        @relation software metric

        @attribute number_of_files numeric
        @attribute "lines of code" numeric
        @attribute 'defect density' numeric

        @data 10,10,10
        '''
        loads = self.get_loads()

        # The string must be quoted if the name includes spaces.
        with self.assertRaisesRegexp(arff.BadRelationFormat, "Bad @RELATION format, at line 1\.$"):
          obj = loads(ARFF_FORMAT_ERROR_RELATION)


    def test_format_error_attribute(self):
        ARFF_FORMAT_ERROR_ATTRIBUTE = '''\
        @relation "software metric"

        @attribute #_of_files numeric
        @attribute lines of code numeric
        @attribute defect density numeric

        @data 10,10,10
        '''

        loads = self.get_loads()

        # the <attribute-name> must start with an alphabetic character.
        with self.assertRaisesRegexp(arff.BadAttributeFormat, "Bad @ATTRIBUTE format, at line 3\.$"):
          obj = loads(ARFF_FORMAT_ERROR_ATTRIBUTE)

