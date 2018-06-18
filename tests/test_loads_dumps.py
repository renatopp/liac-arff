import os
import unittest
import arff
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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
'''

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

        count = 0
        while count < 10:
            count += 1

            obj = loads(arff)
            arff = dumps(obj)
            self.assertEqual(arff, ARFF)

    def test_issue_69(self):
        # https://github.com/renatopp/liac-arff/issues/69
        example_arff_file = os.path.join(os.path.dirname(__file__), 'examples', 'issue69.arff')
        with open(example_arff_file) as fh:
            string = fh.read()

        obj = self.get_loads()(string)

        for i in range(10):
            tmp_obj = self.get_loads()(string)
            tmp_string = self.get_dumps()(tmp_obj)
            new_obj = self.get_loads()(tmp_string)
            self.assertEqual(new_obj, obj)
