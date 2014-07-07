import unittest
import arff

class TestDecodeAttributeTypes(unittest.TestCase):
    def get_decoder(self):
        decoder = arff.ArffDecoder()
        return decoder

    def test_numeric(self):
        '''Numeric attributes.'''
        decoder = self.get_decoder()

        # Simple case
        fixture = u'@ATTRIBUTE attribute-name NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'NUMERIC')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

        # Case insensitive
        fixture = u'@ATTRIBUTE attribute-name NuMeriC'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'NUMERIC')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

    def test_real(self):
        '''Real attributes.'''
        decoder = self.get_decoder()

        # Simple case
        fixture = u'@ATTRIBUTE attribute-name REAL'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'REAL')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

        # Case insensitive
        fixture = u'@ATTRIBUTE attribute-name ReAl'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'REAL')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

    def test_integer(self):
        '''Integer attributes.'''
        decoder = self.get_decoder()

        # Simple case
        fixture = u'@ATTRIBUTE attribute-name INTEGER'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'INTEGER')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

        # Case insensitive
        fixture = u'@ATTRIBUTE attribute-name InteGeR'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'INTEGER')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

    def test_string(self):
        '''String attributes.'''
        decoder = self.get_decoder()

        # Simple case
        fixture = u'@ATTRIBUTE attribute-name STRING'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'STRING')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

        # Case insensitive
        fixture = u'@ATTRIBUTE attribute-name stRing'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', u'STRING')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])

    def test_nominal(self):
        '''Nominal attributes.'''
        decoder = self.get_decoder()

        # Simple case
        fixture = u'@ATTRIBUTE attribute-name {a, b, c}'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', [u'a', u'b', u'c'])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(len(result[1]), 3)
        self.assertEqual(result[1][0], expected[1][0])
        self.assertEqual(result[1][1], expected[1][1])
        self.assertEqual(result[1][2], expected[1][2])

        # Quoted/Spaced/Number case
        fixture = u'@ATTRIBUTE attribute-name {"name with spce", 1,    lol,2 }'
        result = decoder._decode_attribute(fixture)
        expected = (u'attribute-name', [u'name with spce', u'1', u'lol', u'2'])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(len(result[1]), 4)
        self.assertEqual(result[1][0], expected[1][0])
        self.assertEqual(result[1][1], expected[1][1])
        self.assertEqual(result[1][2], expected[1][2])
        self.assertEqual(result[1][3], expected[1][3])


    def test_invalid_type(self):
        '''Invalid type name or structure.'''
        decoder = self.get_decoder()

        # Invalid type name
        fixture = u'@ATTRIBUTE attribute-name NON-EXIST'
        self.assertRaises(
            arff.BadAttributeType, 
            decoder._decode_attribute,
            fixture
        )

        # Invalid nominal structure
        fixture = u'@ATTRIBUTE attribute-name {1, 2] 3'
        self.assertRaises(
            arff.BadAttributeType, 
            decoder._decode_attribute,
            fixture
        )

