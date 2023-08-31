import unittest
import arff


class TestEncodeRelation(unittest.TestCase):
    def get_encoder(self):
        decoder = arff.ArffEncoder()
        return decoder

    def test_simple(self):
        '''Relation name without spaces.'''
        encoder = self.get_encoder()

        fixture = 'relation-name'
        result = encoder._encode_relation(fixture)
        expected = '@RELATION relation-name'

        self.assertEqual(result, expected)

    def test_espaced(self):
        '''Relation name with spaces.'''
        encoder = self.get_encoder()

        fixture = 'relation name and'
        result = encoder._encode_relation(fixture)
        expected = '@RELATION "relation name and"'

        self.assertEqual(result, expected)

    def test_special(self):
        '''Relation name with spaces.'''
        encoder = self.get_encoder()

        fixture = '%relationnameand'
        result = encoder._encode_relation(fixture)
        expected = '@RELATION "%relationnameand"'

        self.assertEqual(result, expected)

        fixture = 'relation,nameand'
        result = encoder._encode_relation(fixture)
        expected = '@RELATION "relation,nameand"'

        self.assertEqual(result, expected)
