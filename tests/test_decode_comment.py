import unittest
import arff

class TestDecodeComment(unittest.TestCase):
    def get_decoder(self):
        decoder = arff.ArffDecoder()
        return decoder

    def test_simple(self):
        '''Comments without any space padding or special characters.'''
        decoder = self.get_decoder()

        fixture = u'%This is a simple comment.'

        result = decoder._decode_comment(fixture)
        expected = u'This is a simple comment.'

        self.assertEqual(result, expected)

    def test_padding(self):
        '''Comments with space padding right after the % character.'''
        decoder = self.get_decoder()

        fixture = u'% This is a simple comment.'

        result = decoder._decode_comment(fixture)
        expected = u'This is a simple comment.'

        self.assertEqual(result, expected)
