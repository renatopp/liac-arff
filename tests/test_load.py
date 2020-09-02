import unittest
import arff
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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

class TestLoad(unittest.TestCase):
    def get_load(self):
        load = arff.load
        return load

    def test_simple(self):
        load = self.get_load()

        file_ = StringIO(ARFF)
        obj = load(file_)

        self.assertEqual(obj['description'], 'XOR Dataset')
        self.assertEqual(obj['relation'], 'XOR')
        self.assertEqual(obj['attributes'][0][0], 'input1')
        self.assertEqual(obj['attributes'][0][1], 'REAL')
        self.assertEqual(obj['data'][0][0], 0.0)
        self.assertEqual(obj['data'][0][1], 0.0)
        self.assertEqual(obj['data'][0][2], 0.0)

