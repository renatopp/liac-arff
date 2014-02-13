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
% 
% 
% '''

OBJ = {
    u'description':u'\nDESCRIPTION HERE\n',
    u'relation': u'weather',
    u'attributes': [
        (u'outlook', [u'sunny', u'overcast', u'rainy']),
        (u'temperature', 'REAL'),
        (u'humidity', 'REAL'),
        (u'windy', [u'TRUE', u'FALSE']),
        (u'play', [u'yes', u'no'])
    ],
    u'data': [
        [u'sunny', 85.0, 85.0, u'FALSE', u'no'],
        [u'sunny', 80.0, 90.0, u'TRUE', u'no'],
        [u'overcast', 83.0, 86.0, u'FALSE', u'yes'],
        [u'rainy', 70.0, 96.0, u'FALSE', u'yes'],
        [u'rainy', 68.0, 80.0, u'FALSE', u'yes'],
        [u'rainy', 65.0, 70.0, u'TRUE', u'no'],
        [u'overcast', 64.0, 65.0, u'TRUE', u'yes'],
        [u'sunny', 72.0, 95.0, u'FALSE', u'no'],
        [u'sunny', 69.0, 70.0, u'FALSE', u'yes'],
        [u'rainy', 75.0, 80.0, u'FALSE', u'yes'],
        [u'sunny', 75.0, 70.0, u'TRUE', u'yes'],
        [u'overcast', 72.0, 90.0, u'TRUE', u'yes'],
        [u'overcast', 81.0, 75.0, u'FALSE', u'yes'],
        [u'rainy', 71.0, 91.0, u'TRUE', u'no']
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

        fixture = {'attributes':[('name','REAL')], 'data':[[1]]}
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {'relation':'name', 'data':[[1]]}
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {'relation':'name', 'attributes':[('name','REAL')]}
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

    def test_invalid_object_attribute(self):
        encoder = self.get_encoder()

        fixture = {
            'relation':'name', 
            'attributes':[4],
            'data':[[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )
        
        fixture = {
            'relation':'name', 
            'attributes':[(2, 'REAL')],
            'data':[[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {
            'relation':'name', 
            'attributes':[('NAME', 'REAL', 'MORE')],
            'data':[[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )

        fixture = {
            'relation':'name', 
            'attributes':[('NAME', 3)],
            'data':[[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )


    def test_attribute_invalid_attribute_type(self):
        encoder = self.get_encoder()

        fixture = {
            'relation':'name', 
            'attributes':[('name','INVALID')], 
            'data':[[1]]
        }
        self.assertRaises(
            arff.BadObject,
            encoder.encode,
            fixture
        )



