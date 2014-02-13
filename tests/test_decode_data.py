import unittest
import arff

class ConversorStub(object):
    def __init__(self, r_value):
        self.r_value = r_value

    def __call__(self, value):
        return self.r_value(value)

class TestDecodeData(unittest.TestCase):
    def get_decoder(self, conversors):
        decoder = arff.ArffDecoder()
        decoder._conversors = conversors
        return decoder

    def test_conversor(self):
        '''Basic data instances.'''
        decoder = self.get_decoder([
            ConversorStub(unicode),
            ConversorStub(float),
            ConversorStub(int),
            ConversorStub(unicode),
        ])

        fixture = u'Iris,3.4,2,Setosa'
        result = decoder._decode_data(fixture)
        expected = [u'Iris', 3.4, 2, u'Setosa']

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])
        self.assertEqual(result[2], expected[2])
        self.assertEqual(result[3], expected[3])
