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
        obj = None

        count = 0
        while count < 10:
            count += 1

            obj = loads(arff)
            arff = dumps(obj)
            self.assertEqual(arff, ARFF)

    def test_date(self):
        file_ = '''@RELATION employee
        @ATTRIBUTE Name STRING
        @ATTRIBUTE start_date DATE
        @ATTRIBUTE end_date DATE '%Y/%m/%dT%H:%M:%S'
        @ATTRIBUTE simple_date DATE '%Y/%m/%d'        
        @DATA
        Lulu,'2011-05-20T12:34:56','2014/06/21T12:34:56','2018/03/04'
        Daisy,'2012-09-30T12:34:56','2015/11/21T12:34:56','2018/03/04'
        Brie,'2013-05-01T12:34:56','2016/12/21T12:34:56','2018/03/04'
        '''
        decoder = arff.ArffDecoder()
        d = decoder.decode(file_, encode_nominal=True)
        reconstituted = arff.dumps(d)
        decoder2 = arff.ArffDecoder()
        d2 = decoder2.decode(reconstituted, encode_nominal=True)
        self.assertEqual(d['data'][1][1] , d2['data'][1][1])
        self.assertEqual(d['data'][1][2] , d2['data'][1][2])
        self.assertEqual(d['data'][1][3] , d2['data'][1][3])
        self.assertEqual(d['data'][2][1], d2['data'][2][1])
        self.assertEqual(d['data'][2][2], d2['data'][2][2])
        self.assertEqual(d['data'][2][3], d2['data'][2][3])
