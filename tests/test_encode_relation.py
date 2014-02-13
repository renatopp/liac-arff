import unittest
import arff

class TestEncodeRelation(unittest.TestCase):
    def get_encoder(self):
        decoder = arff.ArffEncoder()
        return decoder

    def test_simple(self):
        '''Relation name without spaces.'''
        encoder = self.get_encoder()

        fixture = u'relation-name'
        result = encoder._encode_relation(fixture)
        expected = u'@RELATION relation-name'

        self.assertEqual(result, expected)

    def test_espaced(self):
        '''Relation name with spaces.'''
        encoder = self.get_encoder()

        fixture = u'relation name and'
        result = encoder._encode_relation(fixture)
        expected = u'@RELATION "relation name and"'

        self.assertEqual(result, expected)

