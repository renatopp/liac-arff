import unittest
import arff

class TestDecodeRelation(unittest.TestCase):
    def get_decoder(self):
        decoder = arff.ArffDecoder()
        return decoder

    def test_simple(self):
        '''Relation names without spaces.'''
        decoder = self.get_decoder()

        fixture = u'@RELATION relation-name'
        result = decoder._decode_relation(fixture)
        expected = u'relation-name'

        self.assertEqual(result, expected)

    def test_padding(self):
        '''Relation names with padding between @RELATION and the value.'''
        decoder = self.get_decoder()

        fixture = u'@RELATION     relation-name'
        result = decoder._decode_relation(fixture)
        expected = u'relation-name'

        self.assertEqual(result, expected)

    def test_quotes(self):
        '''Quoted relation names and without space in the name.'''
        decoder = self.get_decoder()

        # double quoted
        fixture = u'@RELATION "relation-name"'
        result = decoder._decode_relation(fixture)
        expected = u'relation-name'

        self.assertEqual(result, expected)

        # simple quoted
        fixture = u"@RELATION 'relation-name'"
        result = decoder._decode_relation(fixture)
        expected = u'relation-name'

        self.assertEqual(result, expected)

    def test_spaces(self):
        '''Quoted relation names with spaces in the name.'''
        decoder = self.get_decoder()

        # double quoted
        fixture = u'@RELATION "relation name"'
        result = decoder._decode_relation(fixture)
        expected = u'relation name'

        self.assertEqual(result, expected)

        # simple quoted
        fixture = u"@RELATION 'relation name'"
        result = decoder._decode_relation(fixture)
        expected = u'relation name'

        self.assertEqual(result, expected)

    def test_invalid_spaces(self):
        '''Relation names with spaces and without quotes.'''
        decoder = self.get_decoder()

        fixture = u'@RELATION bad relation name'
        self.assertRaises(
            arff.BadRelationFormat, 
            decoder._decode_relation,
            fixture
        )