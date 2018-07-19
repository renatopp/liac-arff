import unittest
import arff

ARFF_SOURCE = '''% 
@RELATION teste

@ATTRIBUTE a STRING
@ATTRIBUTE b {a, b, c, d}
@ATTRIBUTE c STRING
@ATTRIBUTE d {'"a"', '"b"', '"c"', '"d"'}

@DATA
lorem, b, thisisavalidstatement,'"b"'
lorem, b, 'this is a valid statement with an % symbol','"b"'
lorem2, d, 'this is a valid statement','"d"'
lorem3, c, 'this is a valid statement with double quotes included """""""! ','"c"'
lorem4, a, 'this is a valid statement with singlequotes included \\\' lol \\\'! ','"a"'
'''

ARFF_DESTINY = '''@RELATION teste

@ATTRIBUTE a STRING
@ATTRIBUTE b {a, b, c, d}
@ATTRIBUTE c STRING
@ATTRIBUTE d {\'\\"a\\"\', \'\\"b\\"\', \'\\"c\\"\', \'\\"d\\"\'}

@DATA
lorem,b,thisisavalidstatement,\'\\"b\\"\'
lorem,b,'this is a valid statement with an \\% symbol',\'\\"b\\"\'
lorem2,d,'this is a valid statement',\'\\"d\\"\'
lorem3,c,'this is a valid statement with double quotes included \\"\\"\\"\\"\\"\\"\\"! ',\'\\"c\\"\'
lorem4,a,'this is a valid statement with singlequotes included \\\' lol \\\'! ',\'\\"a\\"\'
'''


class TestDumpEscape(unittest.TestCase):
    def test_encode_source(self):
        obj = arff.loads(ARFF_SOURCE)
        result = arff.dumps(obj)
        expected = ARFF_DESTINY

        self.assertEqual(result, expected)

    def test_encode_destiny(self):
        src = ARFF_DESTINY

        count = 0
        while count < 10:
            count += 1

            obj = arff.loads(src)
            src = arff.dumps(obj)
            self.assertEqual(src, ARFF_DESTINY)

