import unittest
import arff
import StringIO

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

class TestLoads(unittest.TestCase):
    def get_loads(self):
        load = arff.loads
        return load

    def test_simple(self):
        loads = self.get_loads()
        obj = loads(ARFF)

        self.assertEqual(obj['description'], u'XOR Dataset')
        self.assertEqual(obj['relation'], u'XOR')
        self.assertEqual(obj['attributes'][0][0], u'input1')
        self.assertEqual(obj['attributes'][0][1], u'REAL')
        self.assertEqual(obj['data'][0][0], 0.0)
        self.assertEqual(obj['data'][0][1], 0.0)
        self.assertEqual(obj['data'][0][2], 0.0)

