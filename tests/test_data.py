import types
import unittest
import arff


class ConversorStub(object):
    def __init__(self, r_value):
        self.r_value = r_value

    def __call__(self, value):
        return self.r_value(value)


class COOStub(object):
    def __init__(self, data, row, col):
        self.data = data
        self.row = row
        self.col = col


class TestData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]
        self.data = arff.Data()

    # --------------------------------------------------------------------------
    # Tests for the decoding part
    def test_conversor(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode)]

        fixture = u'Iris,3.4,2,Setosa'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        expected = [u'Iris', 3.4, 2, u'Setosa']

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = u'{0 Iris,1 3.4, 2 2}'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        expected = [u'Iris', 3.4, 2, u'0', 0.0, 0]

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = [[1, 3, 'Renato', 'Name with spaces']]
        result = self.data._encode_data(fixture, self.attributes)
        expected = u"1,3,Renato,'Name with spaces'"

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(), expected)

    def test_null_value(self):
        fixture = [[1, None, 'Renato', '']]
        result = self.data._encode_data(fixture, self.attributes)
        expected = u"1,?,Renato,?"

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(), expected)

    def test_too_short(self):
        fixture = [[1, None]]
        generator = self.data._encode_data(fixture, self.attributes)
        self.assertRaises(arff.BadObject, generator.next)


class TestCOOData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]

        self.data = arff.COOData()

    # --------------------------------------------------------------------------
    # Tests for the decoding part
    def test_conversor(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode)]

        fixture = u'{0 Iris,1 3.4,2 2,3 Setosa}'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        row = self.data.data[1]
        col = self.data.data[2]
        expected = [u'Iris', 3.4, 2, u'Setosa']

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])
        self.assertEqual(row, [0, 0, 0, 0])
        self.assertEqual(col, [0, 1, 2, 3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = u'{0 Iris,1 3.4, 2 2}'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        expected = {0: u'Iris', 1: 3.4, 2: 2}

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = COOStub([1, None, 'Renato', 'Name with spaces'],
                          [0, 0, 0, 0],
                          [0, 1, 2, 3])
        result = self.data._encode_data(fixture, self.attributes)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(), u'{ 0 1,1 ?,2 Renato,3 \'Name with spaces\' }')


    def test_null_value(self):
        fixture = COOStub([1, None, 'Renato', ''],
                          [0, 0, 0, 0],
                          [0, 1, 2, 3])
        result = self.data._encode_data(fixture, self.attributes)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(), u'{ 0 1,1 ?,2 Renato,3 ? }')

    def test_sparse_matrix(self):
        fixture = COOStub([1, None, 'Renato', ''],
                          [0, 5, 17, 55],
                          [0, 1, 2, 3])
        result = self.data._encode_data(fixture, self.attributes)
        self.assertIsInstance(result, types.GeneratorType)
        lines = [line for line in result]
        self.assertEqual(lines[0], '{ 0 1 }')
        self.assertEqual(lines[1], '{  }')
        self.assertEqual(lines[55], '{ 3 ? }')
        self.assertEqual(len(lines), 56)

    def test_encode_scipy_coo_example(self):
        attributes = (('', ''), ('', ''), ('', ''), ('', ''))

        fixture = COOStub([1, 1, 1, 1, 1, 1, 1],
                [0, 0, 1, 3, 1, 0, 0],
                [0, 2, 1, 3, 1, 0, 0])

        generator = self.data._encode_data(fixture, attributes)
        self.assertRaises(ValueError, generator.next)


class TestLODData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]

        self.data = arff.LODData()

    # --------------------------------------------------------------------------
    # Tests for the decoding part
    def test_conversor(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode)]

        fixture = u'{0 Iris,1 3.4,2 2,3 Setosa}'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        expected = {0: u'Iris', 1: 3.4, 2: 2, 3: u'Setosa'}

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str if arff.PY3 else unicode),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = u'{0 Iris,1 3.4, 2 2}'
        self.data._decode_data(fixture, conversors)
        result = self.data.data[0]
        expected = [u'Iris', 3.4, 2]

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = [{0: 1, 1: None, 2: 'Renato', 3: 'Name with spaces'}]
        result = self.data._encode_data(fixture, self.attributes)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(),
                         u'{ 0 1,1 ?,2 Renato,3 \'Name with spaces\' }')


    def test_null_value(self):
        fixture = [{0: 1, 1: None, 2: 'Renato', 3: ''}]
        result = self.data._encode_data(fixture, self.attributes)

        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(result.next(), u'{ 0 1,1 ?,2 Renato,3 ? }')

    def test_sparse_matrix(self):
        fixture = [{0: 1}]
        fixture.extend([{}] * 4)
        fixture.append({1: None})
        fixture.extend([{}] * 11)
        fixture.append({2: 'Renato'})
        fixture.extend([{}] * 37)
        fixture.append({3: ''})

        result = self.data._encode_data(fixture, self.attributes)
        self.assertIsInstance(result, types.GeneratorType)
        lines = [line for line in result]

        self.assertEqual(lines[0], '{ 0 1 }')
        self.assertEqual(lines[1], '{  }')
        self.assertEqual(lines[55], '{ 3 ? }')
        self.assertEqual(len(lines), 56)