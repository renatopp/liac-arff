import unittest
import arff

class TestEncodeData(unittest.TestCase):
    def get_encoder(self):
        decoder = arff.ArffEncoder()
        return decoder

    def test_simple(self):
        encoder = self.get_encoder()

        fixture = [1, 3, 'Renato', 'Name with spaces']
        result = encoder._encode_data(fixture)
        expected = u"1,3,Renato,'Name with spaces'"

        self.assertEqual(result, expected)

    def test_null_value(self):
        encoder = self.get_encoder()

        fixture = [1, None, 'Renato', '']
        result = encoder._encode_data(fixture)
        expected = u"1,?,Renato,?"

        self.assertEqual(result, expected)

    def test_sparse_value(self):
        encoder = self.get_encoder()
        fixture = [1,None,'li',0]
        result = encoder._encode_data(fixture, is_sparse = True)

        expected = u"{0 1,1 ?,2 li}"
        self.assertEqual(result, expected)
        

