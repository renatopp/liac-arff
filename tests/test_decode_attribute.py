import unittest
import arff


class TestDecodeAttribute(unittest.TestCase):
    def get_decoder(self):
        decoder = arff.ArffDecoder()
        return decoder

    def test_padding(self):
        '''Attributes with spaces between attribute declaration and name, and
        between attribute name and type.'''
        decoder = self.get_decoder()

        fixture = '@ATTRIBUTE      attribute-name       NUMERIC'

        result = decoder._decode_attribute(fixture)
        expected = 'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_quoted(self):
        '''Attributes with quoted name but without space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = '@ATTRIBUTE "attribute-name" NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = 'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

        # Simple Quote
        fixture = "@ATTRIBUTE 'attribute-name' NUMERIC"
        result = decoder._decode_attribute(fixture)
        expected = 'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_numeric_name(self):
        '''Attributes with quoted name but without space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = '@ATTRIBUTE 0 NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = '0'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_quoted_special(self):
        '''Attributes with quoted name but without space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = '@ATTRIBUTE "%attribute-name" NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = '%attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

        # Simple Quote
        fixture = "@ATTRIBUTE ',attribute {} name' NUMERIC"
        result = decoder._decode_attribute(fixture)
        expected = ',attribute {} name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_quoted_space(self):
        '''Attributes with quoted name and space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = '@ATTRIBUTE "attribute name" NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = 'attribute name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

        # Simple Quote
        fixture = "@ATTRIBUTE 'attribute name' NUMERIC"
        result = decoder._decode_attribute(fixture)
        expected = 'attribute name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_invalid_format(self):
        '''Attributes with bad format.'''
        decoder = self.get_decoder()

        fixture = '@ATTRIBUTE badformat'
        self.assertRaises(
            arff.BadAttributeFormat,
            decoder._decode_attribute,
            fixture
        )

        fixture = '@ATTRIBUTE NUMERIC'
        self.assertRaises(
            arff.BadAttributeFormat,
            decoder._decode_attribute,
            fixture
        )

    def test_invalid_characters(self):
        '''Attributes with bad format.'''
        decoder = self.get_decoder()

        fixture = '@ATTRIBUTE %badformat'
        self.assertRaises(
            arff.BadAttributeFormat,
            decoder._decode_attribute,
            fixture
        )

        fixture = '@ATTRIBUTE na,me NUMERIC'
        self.assertRaises(
            arff.BadAttributeFormat,
            decoder._decode_attribute,
            fixture
        )

        fixture = '@ATTRIBUTE {name NUMERIC'
        self.assertRaises(
            arff.BadAttributeFormat,
            decoder._decode_attribute,
            fixture
        )
