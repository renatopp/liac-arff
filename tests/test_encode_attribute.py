import unittest
import arff

class TestEncodeComment(unittest.TestCase):
    def get_encoder(self):
        decoder = arff.ArffEncoder()
        return decoder

    def test_attribute_name(self):
        encoder = self.get_encoder()

        fixture = (u'attribute name', 'REAL')
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE "attribute name" REAL'

        self.assertEqual(result, expected)       

    def test_attribute_real(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', 'REAL')
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name REAL'

        self.assertEqual(result, expected)

    def test_attribute_numeric(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', 'NUMERIC')
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name NUMERIC'

        self.assertEqual(result, expected)

    def test_attribute_integer(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', 'INTEGER')
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name INTEGER'

        self.assertEqual(result, expected)

    def test_attribute_string(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', 'STRING')
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name STRING'

        self.assertEqual(result, expected)

    def test_attribute_nominal(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', ['a', 'b', 'c'])
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name {a, b, c}'

        self.assertEqual(result, expected)

    def test_attribute_nominal_spaced(self):
        encoder = self.get_encoder()

        fixture = (u'attribute-name', ['with space', 'b', 'c'])
        result = encoder._encode_attribute(*fixture)
        expected = u'@ATTRIBUTE attribute-name {"with space", b, c}'

        self.assertEqual(result, expected)
