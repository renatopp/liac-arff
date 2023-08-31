import unittest
import arff

OBJ = {
    'description': 'teste',
    'relation': 'teste',
    'attributes': [
        ('a', 'STRING'),
        ('b', ('a', 'b', 'c', 'd')),
        ('c', 'STRING'),
        ('d', ('"a"', '"b"', '"c"', '"d"')),
    ],
    'data': [
        ['lorem', 'b', 'thisisavalidstatement', '"b"'],
        ['lorem', 'b', 'this is a valid statement with an % symbol', '"b"'],
        ['lorem2', 'd', 'this is a valid statement', '"d"'],
        ['lorem3', 'c', 'this is a valid statement with double quotes included """""""! ', '"c"'],  # noqa: E501
        ['lorem4', 'a', 'this is a valid \\ statement with singlequotes included \' lol \'! ', '"a"'],  # noqa: E501
    ],
}

ARFF = '''% teste
@RELATION teste

@ATTRIBUTE a STRING
@ATTRIBUTE b {a, b, c, d}
@ATTRIBUTE c STRING
@ATTRIBUTE d {\'\\"a\\"\', \'\\"b\\"\', \'\\"c\\"\', \'\\"d\\"\'}

@DATA
lorem,b,thisisavalidstatement,\'\\"b\\"\'
lorem,b,'this is a valid statement with an \\% symbol',\'\\"b\\"\'
lorem2,d,'this is a valid statement',\'\\"d\\"\'
lorem3,c,'this is a valid statement with double quotes included \\"\\"\\"\\"\\"\\"\\"! ',\'\\"c\\"\'
lorem4,a,'this is a valid \\\\ statement with singlequotes included \\\' lol \\\'! ',\'\\"a\\"\'
'''  # noqa: E501


class TestDumps(unittest.TestCase):
    def get_dumps(self):
        dumps = arff.dumps
        return dumps

    def test_simple(self):
        dumps = self.get_dumps()
        s = dumps(OBJ)
        self.assertEqual(s, ARFF)

        count = 0
        while count < 10:
            count += 1
            obj = arff.loads(s)
            src = arff.dumps(obj)
            self.assertEqual(src, ARFF)
