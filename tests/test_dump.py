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

class TestDump(unittest.TestCase):
    def get_dump(self):
        dump = arff.dump
        return dump

    def test_simple(self):
        dump = self.get_dump()
        fp = StringIO.StringIO()

        s = dump(OBJ, fp)

        fp.seek(0)
        self.assertEqual(fp.read(), ARFF)

