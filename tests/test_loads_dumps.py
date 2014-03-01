import unittest
import arff
import StringIO

OBJ = {
    'description': '\nXOR Dataset\n\n\n',
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

ARFF = '''% 
% XOR Dataset
% 
% 
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

class TestLoadDump(unittest.TestCase):
    def get_dumps(self):
        dumps = arff.dumps
        return dumps

    def get_loads(self):
        loads = arff.loads
        return loads

    def test_simple(self):
        dumps = self.get_dumps()
        loads = self.get_loads()

        arff = ARFF
        obj = None

        count = 0
        while count < 10:
            count += 1

            obj = loads(arff)
            arff = dumps(obj)
            self.assertEqual(arff, ARFF)

