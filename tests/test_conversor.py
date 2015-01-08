import unittest
import arff

class TestDecodeConversor(unittest.TestCase):
    def get_conversor(self, *args, **kwargs):
        conversor = arff.Conversor(*args, **kwargs)
        return conversor

    def test_real(self):
        '''Convert real value.'''
        conversor = self.get_conversor('REAL')

        # From Integer
        fixture = u'45'
        result = conversor(fixture)
        expected = 45.0

        self.assertEqual(type(result), float)
        self.assertEqual(result, expected)

        # From Float
        fixture = u'45.13233322'
        result = conversor(fixture)
        expected = 45.13233322

        self.assertEqual(type(result), float)
        self.assertEqual(result, expected)

    def test_numeric(self):
        '''Convert real value.'''
        conversor = self.get_conversor('NUMERIC')

        # From Integer
        fixture = u'45'
        result = conversor(fixture)
        expected = 45.0

        self.assertEqual(type(result), float)
        self.assertEqual(result, expected)

        # From Float
        fixture = u'45.13233322'
        result = conversor(fixture)
        expected = 45.13233322

        self.assertEqual(type(result), float)
        self.assertEqual(result, expected)

    def test_integer(self):
        '''Convert real value.'''
        conversor = self.get_conversor('INTEGER')

        # From Integer
        fixture = u'45'
        result = conversor(fixture)
        expected = 45

        self.assertEqual(type(result), int)
        self.assertEqual(result, expected)

        # From Float
        fixture = u'"45.13233322"'
        result = conversor(fixture)
        expected = 45

        self.assertEqual(type(result), int)
        self.assertEqual(result, expected)

    def test_string(self):
        '''Convert string value.'''
        conversor = self.get_conversor('STRING')

        fixture = u'raposa'
        result = conversor(fixture)
        expected = u'raposa'
        self.assertEqual(result, expected)

        fixture = u'"raposa"'
        result = conversor(fixture)
        expected = u'raposa'
        self.assertEqual(result, expected)

    def test_nominal(self):
        '''Convert nominal value.'''
        conversor = self.get_conversor('NOMINAL', [u'a', u'b', u'3.4'])

        fixture = u'a'
        result = conversor(fixture)
        expected = u'a'
        self.assertEqual(result, expected)

        fixture = u'3.4'
        result = conversor(fixture)
        expected = u'3.4'
        self.assertEqual(result, expected)

    def test_encoded_nominal(self):
        '''Convert nominal to encoded nominal value.'''
        conversor = self.get_conversor('ENCODED_NOMINAL', [u'a', u'b', u'3.4'])

        fixtures_and_expectations = [(u'a', 0), (u'b', 1), (u'3.4', 2)]
        for fixture, expected in fixtures_and_expectations:
            result = conversor(fixture)
            self.assertEqual(result, expected)

    def test_null_value(self):
        '''Values such as "?", or "".'''
        conversor = self.get_conversor('NOMINAL', [u'a', u'b', u'3.4'])
        result = conversor('?')
        expected = None
        self.assertEqual(result, expected)

        result = conversor('')
        expected = None
        self.assertEqual(result, expected)

        conversor = self.get_conversor('ENCODED_NOMINAL', [u'a', u'b', u'3.4'])
        result = conversor('?')
        expected = None
        self.assertEqual(result, expected)

        result = conversor('')
        expected = None
        self.assertEqual(result, expected)

        conversor = self.get_conversor('INTEGER')
        result = conversor('?')
        expected = None
        self.assertEqual(result, expected)

        result = conversor('')
        expected = None
        self.assertEqual(result, expected)

    def test_padding_value(self):
        '''Values such "    3.1415   "'''
        conversor = self.get_conversor('NUMERIC')

        # From Integer
        fixture = u'      45     '
        result = conversor(fixture)
        expected = 45.0

        self.assertEqual(type(result), float)
        self.assertEqual(result, expected)


    def test_invalid_type(self):
        '''Invalid type_ parameter.'''
        self.assertRaises(
            arff.BadAttributeType,
            self.get_conversor,
            'ABACATE'
        )

    def test_invalid_nominal_value(self):
        '''Invalid nominal value.'''
        conversor = self.get_conversor('NOMINAL', [u'a', u'b', u'3.4'])

        self.assertRaises(
            arff.BadNominalValue,
            conversor,
            'ABACATE'
        )

    def test_invalid_numerical_value(self):
        '''Invalid numerical value.'''
        conversor = self.get_conversor('REAL')
        self.assertRaises(
            arff.BadNumericalValue,
            conversor,
            'ABACATE'
        )

        conversor = self.get_conversor('NUMERIC')
        self.assertRaises(
            arff.BadNumericalValue,
            conversor,
            'ABACATE'
        )

        conversor = self.get_conversor('INTEGER')
        self.assertRaises(
            arff.BadNumericalValue,
            conversor,
            'ABACATE'
        )
