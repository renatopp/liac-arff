import unittest
import textwrap
import arff


class BaseTestDecodeConversor(object):

    # Note that we want to test the normalisation (e.g. handling of missing
    # values and quoting), as well as conversion from string to value type.
    # As such, we test the full loading process in several variants.
    # See implementations of get_conversor below.

    def _get_arff_loader(self, return_type, type_, values=None):
        encode_nominal = type_ == 'ENCODED_NOMINAL'
        if values is not None:
            type_ = u'{' + u','.join(values) + u'}'

        def load(value):
            if self.use_sparse:
                data = '{ 0 %s }' % value
            else:
                data = '%s,0' % value
            txt = textwrap.dedent(u'''
            @RELATION testing

            @ATTRIBUTE name {type_}
            @ATTRIBUTE dummy REAL

            @DATA
            {data}
            '''.format(type_=type_, data=data))
            return arff.load(txt, return_type=return_type,
                             encode_nominal=encode_nominal)
        return load

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


class TestDecodeConversorDense(BaseTestDecodeConversor, unittest.TestCase):
    use_sparse = False

    def get_conversor(self, type_, values=None):
        load = self._get_arff_loader(arff.DENSE, type_, values)

        def conversor(value):
            data = load(value)['data']
            assert len(data) == 1
            assert len(data[0]) == 2
            assert data[0][1] == 0
            return data[0][0]
        return conversor


class TestDecodeConversorSparseDense(TestDecodeConversorDense):
    use_sparse = True


class TestDecodeConversorCOO(BaseTestDecodeConversor, unittest.TestCase):
    use_sparse = True

    def get_conversor(self, type_, values=None):
        load = self._get_arff_loader(arff.COO, type_, values)

        def conversor(value):
            data, row, col = load(value)['data']
            assert len(row) == len(col) == len(data) == 1
            assert row == [0]
            assert col == [0]
            return data[0]
        return conversor


class TestDecodeConversorLOD(BaseTestDecodeConversor, unittest.TestCase):
    use_sparse = True

    def get_conversor(self, type_, values=None):
        load = self._get_arff_loader(arff.LOD, type_, values)

        def conversor(value):
            data = load(value)['data']
            assert len(data) == 1
            assert isinstance(data[0], dict)
            assert len(data[0]) == 1
            return data[0][0]
        return conversor
