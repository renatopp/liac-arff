import textwrap
import unittest
import arff

ARFF = '''% 
% DESCRIPTION HERE
% 
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
'''

description = u'\nDESCRIPTION HERE\n'
relation = u'weather'
attributes = [
    (u'outlook', [u'sunny', u'overcast', u'rainy']),
    (u'temperature', 'REAL'),
    (u'humidity', 'REAL'),
    (u'windy', [u'TRUE', u'FALSE']),
    (u'play', [u'yes', u'no'])
    ]
data = [
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
]
encoded_data = [
    [0, 85.0, 85.0, 1, 1],
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
    [2, 71.0, 91.0, 0, 1]
]

OBJ = {
    u'description': description,
    u'relation': relation,
    u'attributes': attributes,
    u'data': data
}

ENCODED_OBJ = {
    u'description': description,
    u'relation': relation,
    u'attributes': attributes,
    u'data': encoded_data
}

xor_dataset = '''% XOR Dataset
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
'''

xor_description = u'XOR Dataset'
xor_relation = u'XOR'
xor_attributes = [(u'input1', u'REAL'),
                  (u'input2', u'REAL'),
                  (u'y', u'REAL')]
xor_data_coo = ([1., 1., 1., 1., 1., 1.],
            [1, 1, 2, 2, 3, 3],
            [1, 2, 0, 2, 0, 1])
xor_data_lod = [{},
                {1: 1., 2: 1.},
                {0: 1., 2: 1.},
                {0: 1., 1: 1.}]
xor_object_coo = {
    u'description': xor_description,
    u'relation': xor_relation,
    u'attributes': xor_attributes,
    u'data': xor_data_coo
}

xor_object_lod = {
    u'description': xor_description,
    u'relation': xor_relation,
    u'attributes': xor_attributes,
    u'data': xor_data_lod
}


class TestDecodeComment(unittest.TestCase):
    def get_decoder(self):
        decoder = arff.ArffDecoder()
        return decoder

    def test_decode(self):
        decoder = self.get_decoder()

        result = decoder.decode(ARFF)
        expected = OBJ

        self.assertEqual(result['description'], expected['description'])
        self.assertEqual(result['relation'], expected['relation'])

        self.assertEqual(len(result['attributes']), len(expected['attributes']))
        self.assertEqual(result['attributes'][0][0], expected['attributes'][0][0])
        self.assertEqual(result['attributes'][0][1][0], expected['attributes'][0][1][0])
        self.assertEqual(result['attributes'][0][1][1], expected['attributes'][0][1][1])
        self.assertEqual(result['attributes'][0][1][2], expected['attributes'][0][1][2])

        self.assertEqual(result['attributes'][1][1], expected['attributes'][1][1])

        self.assertEqual(len(result['data']), len(expected['data']))
        self.assertEqual(result['data'][0][0], expected['data'][0][0])
        self.assertEqual(result['data'][0][1], expected['data'][0][1])
        self.assertEqual(result['data'][0][2], expected['data'][0][2])
        self.assertEqual(result['data'][0][3], expected['data'][0][3])
        self.assertEqual(result['data'][0][4], expected['data'][0][4])

    def test_decode_with_label_encoding(self):
        decoder = self.get_decoder()

        result = decoder.decode(ARFF, True)
        expected = ENCODED_OBJ

        self.assertEqual(result['description'], expected['description'])
        self.assertEqual(result['relation'], expected['relation'])

        self.assertEqual(len(result['attributes']), len(expected['attributes']))
        self.assertEqual(result['attributes'][0][0], expected['attributes'][0][0])
        self.assertEqual(result['attributes'][0][1][0], expected['attributes'][0][1][0])
        self.assertEqual(result['attributes'][0][1][1], expected['attributes'][0][1][1])
        self.assertEqual(result['attributes'][0][1][2], expected['attributes'][0][1][2])

        self.assertEqual(result['attributes'][1][1], expected['attributes'][1][1])

        self.assertEqual(len(result['data']), len(expected['data']))
        self.assertEqual(result['data'][0][0], expected['data'][0][0])
        self.assertEqual(result['data'][0][1], expected['data'][0][1])
        self.assertEqual(result['data'][0][2], expected['data'][0][2])
        self.assertEqual(result['data'][0][3], expected['data'][0][3])
        self.assertEqual(result['data'][0][4], expected['data'][0][4])

    def test_decode_xor_sparse_coo(self):
        decoder = self.get_decoder()

        result = decoder.decode(xor_dataset, return_type=arff.COO)
        expected = xor_object_coo

        self.assertEqual(result, expected)

    def test_decode_xor_sparse_lod(self):
        decoder = self.get_decoder()

        result = decoder.decode(xor_dataset, return_type=arff.LOD)
        expected = xor_object_lod

        self.assertEqual(result, expected)

    def test_invalid_layout(self):
        decoder = self.get_decoder()

        self.assertRaises(
            arff.BadLayout,
            decoder.decode,
            '''
            @data
            @relation name
            '''
        )

        self.assertRaises(
            arff.BadLayout,
            decoder.decode,
            '''
            @attribute name REAL
            '''
        )

        self.assertRaises(
            arff.BadLayout,
            decoder.decode,
            '''
            @data
            '''
        )

        self.assertRaises(
            arff.BadLayout,
            decoder.decode,
            '''
            @relation name
            @attribute name REAL
            1,2,3
            '''
        )

    def test_invalid_data_len(self):
        '''When there is more (or less) data then attributes.'''
        decoder = self.get_decoder()

        self.assertRaises(
            arff.BadDataFormat,
            decoder.decode,
            '''
            @relation name
            @attributes name1 REAL
            @attributes name2 REAL
            @data
            1,2,3
            '''
        )

        self.assertRaises(
            arff.BadDataFormat,
            decoder.decode,
            '''
            @relation name
            @attributes name1 REAL
            @attributes name2 REAL
            @data
            1
            '''
        )


too_many_attributes = '''
@RELATION PR78

@ATTRIBUTE attr1 STRING
@ATTRIBUTE attr2 STRING

@DATA

{0 a}
{1 a}
{2 a}
'''


class TestTooManyAttributes(unittest.TestCase):
    def test_dense(self):
        decoder = arff.ArffDecoder()
        with self.assertRaisesRegexp(arff.BadDataFormat,
                                     'Bad @DATA instance format in line 10: '
                                     '\{2 a\}'):
            decoder.decode(too_many_attributes, return_type=arff.DENSE)

    def test_coo(self):
        decoder = arff.ArffDecoder()
        with self.assertRaisesRegexp(arff.BadDataFormat,
                                     'Bad @DATA instance format in line 10: '
                                     '\{2 a\}'):
            decoder.decode(too_many_attributes, return_type=arff.COO)

    def test_lod(self):
        decoder = arff.ArffDecoder()
        with self.assertRaisesRegexp(arff.BadDataFormat,
                                     'Bad @DATA instance format in line 10: '
                                     '\{2 a\}'):
            decoder.decode(too_many_attributes, return_type=arff.LOD)


duplicate_attribute = '''@RELATION test

@ATTRIBUTE attr1 INTEGER
@ATTRIBUTE attr1 INTEGER

@DATA
1, 2
'''


class TestDuplicateAttributeName(unittest.TestCase):
    def test_decode(self):
        decoder = arff.ArffDecoder()
        with self.assertRaisesRegexp(arff.BadAttributeName,
                                     'Bad @ATTRIBUTE name attr1 at line 4, '
                                     'this name is already in use in line 3.'):
            decoder.decode(duplicate_attribute)


class TestInvalidValues(unittest.TestCase):
    def setUp(self):
        self.my_arff = textwrap.dedent(u'''
        @RELATION testing
        
        @ATTRIBUTE attr1 STRING
        @ATTRIBUTE attr2 {{'a b', 'c d'}}
        
        @DATA
        
        {data}
        ''')

    def test_dense(self):


        fixture = self.my_arff.format(data="a','c d'")
        with self.assertRaisesRegexp(ValueError,
                                     "Expected comma or whitespace at position "
                                     "4, not c for line a','c d'."):
            arff.load(fixture)

        fixture = self.my_arff.format(data="a b, 'c d'")
        with self.assertRaisesRegexp(arff.BadStringValue,
                                     "Invalid string value at line 8."):
            print(arff.load(fixture))

        fixture = self.my_arff.format(data="'a b', c d")
        with self.assertRaisesRegexp(arff.BadNominalFormatting,
                                     'Nominal data value "c d" not properly '
                                     'quoted in line 8'):
            print(arff.load(fixture))

    def test_sparse(self):

        fixture = self.my_arff.format(data="{0 a',1 'c d'}")
        with self.assertRaisesRegexp(arff.ArffException,
                                     ".*',1 'c d'}."):
            arff.load(fixture)

        fixture = self.my_arff.format(data="{0 a b,1 'c d'}")
        with self.assertRaisesRegexp(arff.ArffException,
                                     ".*b,1 'c d'"):
            print(arff.load(fixture))

        fixture = self.my_arff.format(data="{0 'a b', 1 c d}")
        with self.assertRaisesRegexp(arff.ArffException,
                                     r'.*d\}'):
            print(arff.load(fixture))
