import types
import unittest
import arff

from unittest import mock


class ConversorStub:
    def __init__(self, r_value):
        self.r_value = r_value

    def __call__(self, value):
        return self.r_value(value)


class COOStub:
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
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str)]

        fixture = 'Iris,3.4,2,Setosa'
        result, = self.data.decode_rows([fixture], conversors)
        expected = ['Iris', 3.4, 2, 'Setosa']

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = '{0 Iris,1 3.4, 2 2}'
        result, = self.data.decode_rows([fixture], conversors)
        expected = ['Iris', 3.4, 2, '0', 0.0, 0]

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = [[1, 3, 'Renato', 'Name with spaces']]
        result = self.data.encode_data(fixture, self.attributes)
        expected = "1,3,Renato,'Name with spaces'"

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result), expected)

    def test_null_value(self):
        fixture = [[1, None, 'Renato', '']]
        result = self.data.encode_data(fixture, self.attributes)
        expected = "1,?,Renato,?"

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result), expected)

    def test_too_short(self):
        fixture = [[1, None]]
        generator = self.data.encode_data(fixture, self.attributes)
        self.assertRaises(arff.BadObject, next, generator)

    def test_encode_too_many_attributes_dense(self):
        my_arff = {
            "attributes": [["attr", "INTEGER"]],
            "data": [[0], [1, 2]],
            "relation": 'Too many attributes'
        }

        encoder = arff.ArffEncoder()
        with self.assertRaisesRegex(arff.BadObject,
                                    "Instance 1 has 2 attributes, expected 1"):
            encoder.encode(my_arff)


class TestCOOData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]

        self.data = arff.COOData()

    # --------------------------------------------------------------------------
    # Tests for the decoding part
    def test_conversor(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str)]

        fixture = '{0 Iris,1 3.4,2 2,3 Setosa}'
        result, row, col = self.data.decode_rows([fixture], conversors)
        expected = ['Iris', 3.4, 2, 'Setosa']

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])
        self.assertEqual(row, [0, 0, 0, 0])
        self.assertEqual(col, [0, 1, 2, 3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = '{0 Iris,1 3.4, 2 2}'
        result, row, col = self.data.decode_rows([fixture], conversors)
        expected = {0: 'Iris', 1: 3.4, 2: 2}

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = COOStub([1, None, 'Renato', 'Name with spaces'],
                          [0, 0, 0, 0],
                          [0, 1, 2, 3])
        result = self.data.encode_data(fixture, self.attributes)

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result),
                         '{ 0 1,1 ?,2 Renato,3 \'Name with spaces\' }')

    def test_null_value(self):
        fixture = COOStub([1, None, 'Renato', ''],
                          [0, 0, 0, 0],
                          [0, 1, 2, 3])
        result = self.data.encode_data(fixture, self.attributes)

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result), '{ 0 1,1 ?,2 Renato,3 ? }')

    def test_sparse_matrix(self):
        fixture = COOStub([1, None, 'Renato', ''],
                          [0, 5, 17, 55],
                          [0, 1, 2, 3])
        result = self.data.encode_data(fixture, self.attributes)
        self.assertTrue(isinstance(result, types.GeneratorType))
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

        generator = self.data.encode_data(fixture, attributes)
        self.assertRaises(ValueError, next, generator)

    def test_encode_too_many_attributes_coo(self):
        coo = COOStub([1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 1, 1, 1, 1, 3],
                      [0, 1, 2, 3, 4, 5, 0])
        coo.format = 'coo'

        my_arff = {
            "attributes": [["attr", "INTEGER"]],
            "data": coo,
            "relation": 'Too many attributes'
        }

        encoder = arff.ArffEncoder()
        with self.assertRaisesRegex(arff.BadObject,
                                    "Instance 1 has at least 2 attributes, "
                                    "expected 1"):
            encoder.encode(my_arff)


class TestLODData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]

        self.data = arff.LODData()

    # --------------------------------------------------------------------------
    # Tests for the decoding part
    def test_conversor(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str)]

        fixture = '{0 Iris,1 3.4,2 2,3 Setosa}'
        result, = self.data.decode_rows([fixture], conversors)
        expected = {0: 'Iris', 1: 3.4, 2: 2, 3: 'Setosa'}

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])

    def test_sparse(self):
        '''Basic data instances.'''
        conversors = [ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int),
                      ConversorStub(str),
                      ConversorStub(float),
                      ConversorStub(int)]

        fixture = '{0 Iris,1 3.4, 2 2}'
        result, = self.data.decode_rows([fixture], conversors)
        expected = ['Iris', 3.4, 2]

        self.assertEqual(len(result), len(expected))
        for i in range(len(expected)):
            self.assertEqual(result[i], expected[i])

    # --------------------------------------------------------------------------
    # Tests for the encoding part
    def test_simple(self):
        fixture = [{0: 1, 1: None, 2: 'Renato', 3: 'Name with spaces'}]
        result = self.data.encode_data(fixture, self.attributes)

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result),
                         '{ 0 1,1 ?,2 Renato,3 \'Name with spaces\' }')

    def test_null_value(self):
        fixture = [{0: 1, 1: None, 2: 'Renato', 3: ''}]
        result = self.data.encode_data(fixture, self.attributes)

        self.assertTrue(isinstance(result, types.GeneratorType))
        self.assertEqual(next(result), '{ 0 1,1 ?,2 Renato,3 ? }')

    def test_sparse_matrix(self):
        fixture = [{0: 1}]
        fixture.extend([{}] * 4)
        fixture.append({1: None})
        fixture.extend([{}] * 11)
        fixture.append({2: 'Renato'})
        fixture.extend([{}] * 37)
        fixture.append({3: ''})

        result = self.data.encode_data(fixture, self.attributes)
        self.assertTrue(isinstance(result, types.GeneratorType))
        lines = [line for line in result]

        self.assertEqual(lines[0], '{ 0 1 }')
        self.assertEqual(lines[1], '{  }')
        self.assertEqual(lines[55], '{ 3 ? }')
        self.assertEqual(len(lines), 56)

    def test_encode_too_many_attributes_lod(self):

        my_arff = {
            "attributes": [["attr", "INTEGER"]],
            "data": [{0: 1}, {1: 2}],
            "relation": 'Too many attributes'
        }

        encoder = arff.ArffEncoder()
        with self.assertRaisesRegex(arff.BadObject,
                                    "Instance 1 has 2 attributes, expected 1"):
            encoder.encode(my_arff)
