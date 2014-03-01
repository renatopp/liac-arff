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

