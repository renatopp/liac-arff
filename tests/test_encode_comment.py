import unittest
import arff


class TestEncodeComment(unittest.TestCase):
    def get_encoder(self):
        decoder = arff.ArffEncoder()
        return decoder

    def test_simple(self):
        encoder = self.get_encoder()

        fixture = 'This is a simple comment.'
        result = encoder._encode_comment(fixture)
        expected = '% This is a simple comment.'

        self.assertEqual(result, expected)
