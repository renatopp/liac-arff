import unittest
import arff


class TestEncodeData(unittest.TestCase):
    def setUp(self):
        self.attributes = [('a1', 'INTEGER'), ('a2', 'INTEGER'),
                           ('a3', 'STRING'), ('a4', 'STRING')]
        self.encoder = arff.ArffEncoder()


    def test_simple(self):
        encoder = self.encoder

        fixture = [1, 3, 'Renato', 'Name with spaces']
        result = encoder._encode_data(fixture, self.attributes)
        expected = u"1,3,Renato,'Name with spaces'"

        self.assertEqual(result, expected)

    def test_null_value(self):
        encoder = self.encoder

        fixture = [1, None, 'Renato', '']
        result = encoder._encode_data(fixture, self.attributes)
        expected = u"1,?,Renato,?"

        self.assertEqual(result, expected)

    def test_too_short(self):
        encoder = self.encoder

        fixture = [1, None]
        self.assertRaises(arff.BadObject, encoder._encode_data, fixture,
                          self.attributes)