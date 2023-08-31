import unittest
import arff

ARFF = '''%
% DESCRIPTION HERE
%
@RELATION weather

@ATTRIBUTE outlook {sunny, overcast, rainy}
@ATTRIBUTE temperature REAL
@ATTRIBUTE humidity REAL
@ATTRIBUTE windy {TRUE, FALSE}
@ATTRIBUTE play {yes, no}

@DATA
sunny,85.0,85.0,FALSE,no
sunny,80.0,90.0,TRUE,no
overcast,83.0,86.0,FALSE,yes
rainy,70.0,96.0,FALSE,yes
rainy,68.0,80.0,FALSE,yes
rainy,65.0,70.0,TRUE,no
overcast,64.0,65.0,TRUE,yes
sunny,72.0,95.0,FALSE,no
sunny,69.0,70.0,FALSE,yes
rainy,75.0,80.0,FALSE,yes
sunny,75.0,70.0,TRUE,yes
overcast,72.0,90.0,TRUE,yes
overcast,81.0,75.0,FALSE,yes
rainy,71.0,91.0,TRUE,no
'''

OBJ = {
    'description': '\nDESCRIPTION HERE\n',
    'relation': 'weather',
    'attributes': [
        ('outlook', ['sunny', 'overcast', 'rainy']),
        ('temperature', 'REAL'),
        ('humidity', 'REAL'),
        ('windy', ['TRUE', 'FALSE']),
        ('play', ['yes', 'no'])
    ],
    'data': [
        ['sunny', 85.0, 85.0, 'FALSE', 'no'],
        ['sunny', 80.0, 90.0, 'TRUE', 'no'],
        ['overcast', 83.0, 86.0, 'FALSE', 'yes'],
        ['rainy', 70.0, 96.0, 'FALSE', 'yes'],
        ['rainy', 68.0, 80.0, 'FALSE', 'yes'],
        ['rainy', 65.0, 70.0, 'TRUE', 'no'],
        ['overcast', 64.0, 65.0, 'TRUE', 'yes'],
        ['sunny', 72.0, 95.0, 'FALSE', 'no'],
        ['sunny', 69.0, 70.0, 'FALSE', 'yes'],
        ['rainy', 75.0, 80.0, 'FALSE', 'yes'],
        ['sunny', 75.0, 70.0, 'TRUE', 'yes'],
        ['overcast', 72.0, 90.0, 'TRUE', 'yes'],
        ['overcast', 81.0, 75.0, 'FALSE', 'yes'],
        ['rainy', 71.0, 91.0, 'TRUE', 'no']
    ]
}


class TestEncodeComment(unittest.TestCase):
    def get_encoder(self):
        encoder = arff.ArffEncoder()
        return encoder

    def test_encode(self):
        encoder = self.get_encoder()

        result = encoder.encode(OBJ)
        expected = ARFF

        self.assertEqual(result, expected)

    def test_iter_encode(self):
        encoder = self.get_encoder()

        result = encoder.iter_encode(OBJ)
        expected = ARFF.split('\n')

        for r, e in zip(result, expected):
            self.assertEqual(r, e)

    def test_invalid_object(self):
        encoder = self.get_encoder()

        fixture = {'attributes': [('name', 'REAL')], 'data': [[1]]}
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {'relation': 'name', 'data': [[1]]}
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

    def test_invalid_object_attribute(self):
        encoder = self.get_encoder()

        fixture = {
            'relation': 'name',
            'attributes': [4],
            'data': [[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {
            'relation': 'name',
            'attributes': [(2, 'REAL')],
            'data': [[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {
            'relation': 'name',
            'attributes': [('NAME', 'REAL', 'MORE')],
            'data': [[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {
            'relation': 'name',
            'attributes': [('NAME', 3)],
            'data': [[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

    def test_attribute_invalid_attribute_type(self):
        encoder = self.get_encoder()

        fixture = {
            'relation': 'name',
            'attributes': [('name', 'INVALID')],
            'data': [[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

    def test_encode_duplicate_attribute_name(self):
        encoder = self.get_encoder()

        fixture = {
            'relation': 'name',
            'attributes': [('name', 'INTEGER'), ('name', 'INTEGER')],
            'data': [[0], [1]],
        }
        with self.assertRaisesRegex(arff.BadObject,
                                    'Trying to use attribute name "name" '
                                    'for the second time.'):
            encoder.encode(fixture)

    def test_encode_string(self):
        encoder = self.get_encoder()

        fixture = """@RELATION bla

@ATTRIBUTE attr STRING

@DATA
'a,b,c'
'a,b,c '
'a\\\\c'
'a\\"c'
'a\\'c'
'a\\nc'
'a\\tc'
'a\\000c'
'a\\017c'
"""
        my_arff = {
            "attributes": [["attr", "STRING"]],
            "data": [["a,b,c"],
                     ["a,b,c "],
                     ["a\\c"],
                     ["a\"c"],
                     ["a'c"],
                     ["a\nc"],
                     ["a\tc"],
                     ["a\0c"],
                     ["a\017c"],
                     ],
            "relation": "bla"}
        self.assertEqual(encoder.encode(my_arff), fixture)

    def test_encode_adding_quotes_with_spaces(self):
        # regression tests for https://github.com/renatopp/liac-arff/issues/87
        encoder = self.get_encoder()

        # \u3000 corresponds to an ideographic space. It should be treated as
        # a space.
        fixture = {
            'relation': 'name',
            'attributes': [('A', 'STRING'), ('B', 'STRING')],
            'data': [['a', 'b'], ['b\u3000e', 'a']],
        }
        expected_data = """@RELATION name

@ATTRIBUTE A STRING
@ATTRIBUTE B STRING

@DATA
a,b
'b\u3000e',a
"""
        arff_data = encoder.encode(fixture)
        self.assertEqual(arff_data, expected_data)

        decoder = arff.ArffDecoder()
        arff_object = decoder.decode(arff_data)
        self.assertEqual(arff_object['data'], fixture['data'])
