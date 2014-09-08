import unittest
import arff
import StringIO

OBJ = {
    'description': 'XOR Dataset',
    'relation': 'XOR',
    'attributes': [
        ('input1', 'REAL'),
        ('input2', 'REAL'),
        ('y', 'REAL'),
    ],
    'data': [
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0]
    ]
}

ARFF = '''% XOR Dataset
@RELATION XOR

@ATTRIBUTE input1 REAL
@ATTRIBUTE input2 REAL
@ATTRIBUTE y REAL

@DATA
0.0,0.0,0.0
0.0,1.0,1.0
1.0,0.0,1.0
1.0,1.0,0.0
% 
% 
% '''

class TestDumps(unittest.TestCase):
    def get_dumps(self):
        dumps = arff.dumps
        return dumps

    def test_simple(self):
        dumps = self.get_dumps()
        s = dumps(OBJ)

        self.assertEqual(s, ARFF)

