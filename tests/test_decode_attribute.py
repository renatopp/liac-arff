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

        fixture = u'@ATTRIBUTE      attribute-name       NUMERIC'

        result = decoder._decode_attribute(fixture)
        expected = u'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_quoted(self):
        '''Attributes with quoted name but without space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = u'@ATTRIBUTE "attribute-name" NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = u'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

        # Simple Quote
        fixture = u"@ATTRIBUTE 'attribute-name' NUMERIC"
        result = decoder._decode_attribute(fixture)
        expected = u'attribute-name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_quoted_space(self):
        '''Attributes with quoted name and space.'''
        decoder = self.get_decoder()

        # Double Quote
        fixture = u'@ATTRIBUTE "attribute name" NUMERIC'
        result = decoder._decode_attribute(fixture)
        expected = u'attribute name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

        # Simple Quote
        fixture = u"@ATTRIBUTE 'attribute name' NUMERIC"
        result = decoder._decode_attribute(fixture)
        expected = u'attribute name'

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], expected)

    def test_invalid_format(self):
        '''Attributes with bad format.'''
        decoder = self.get_decoder()

        fixture = u'@ATTRIBUTE badformat'
        self.assertRaises(
            arff.BadAttributeFormat, 
            decoder._decode_attribute,
            fixture
        )

        fixture = u'@ATTRIBUTE NUMERIC'
        self.assertRaises(
            arff.BadAttributeFormat, 
            decoder._decode_attribute,
            fixture
        )

