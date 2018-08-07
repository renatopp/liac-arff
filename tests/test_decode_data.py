import unittest
import textwrap
import arff


class TestDecodeLines(unittest.TestCase):
    """Functionally tests the logic of _parse_values

    Focuses on string values, to ignore conversion logic.
    """

    def _load(self, data, n_attribs=1):
        txt = textwrap.dedent(u'''
        @RELATION testing

        {attribs}

        @DATA
        {data}
        ''').format(attribs='\n'.join('@ATTRIBUTE x%d STRING' % i
                                      for i in range(n_attribs)),
                    data=data)
        return arff.load(txt)['data']

    def assertLoadsAs(self, data, expected, n_attribs=1):
        result = self._load(data, n_attribs)
        self.assertListEqual(result, expected)

    def test_quotes(self):
        self.assertLoadsAs("""'ENACT.NOGOPMAJ,2017'""",
                           [['ENACT.NOGOPMAJ,2017']])
        self.assertLoadsAs('''"ENACT.NOGOPMAJ,2017"''',
                           [['ENACT.NOGOPMAJ,2017']])
        self.assertLoadsAs(''' 'A','B' , '"','C,D' ''',
                           [['A', 'B', '"', 'C,D']],
                           n_attribs=4)

    def test_quotes_sparse(self):
        self.assertLoadsAs("""{0 'ENACT.NOGOPMAJ,2017'}""",
                           [['ENACT.NOGOPMAJ,2017']])
        self.assertLoadsAs('''{0 "ENACT.NOGOPMAJ,2017"}''',
                           [['ENACT.NOGOPMAJ,2017']])

        self.assertLoadsAs('''{ 0 'A',1 'B' ,2 '"',3 'C,D' }''',
                           [['A', 'B', '"', 'C,D']],
                           n_attribs=4)

    def test_escapes(self):
        self.assertLoadsAs(r''' '\'' ''',
                           [["'"]])
        self.assertLoadsAs(r''' '\\' ''',
                           [["\\"]])
        self.assertLoadsAs(r''' '\\\'' ''',
                           [["\\'"]])
        self.assertLoadsAs('''"\\\\,",",\\\\"''',
                           [['\\,', ',\\']],
                           n_attribs=2)

    def test_escapes_sparse(self):
        self.assertLoadsAs(r''' {0 '\''} ''',
                           [["'"]])
        self.assertLoadsAs(r''' {0 '\\'} ''',
                           [["\\"]])
        self.assertLoadsAs(r''' {0 '\\\''} ''',
                           [["\\'"]])

    def test_bad_quotes(self):
        self.assertRaises(arff.BadLayout, self._load, r" \'A' ")
        self.assertRaises(arff.BadLayout, self._load, r" \'A ")
        self.assertRaises(arff.BadLayout, self._load, " 'A ")
        self.assertRaises(arff.BadLayout, self._load, ' "A ')
        self.assertRaises(arff.BadLayout, self._load, ' A" ')
        self.assertRaises(arff.BadLayout, self._load, " A' ")
        self.assertRaises(arff.BadLayout, self._load, r" 'A\' ")
        self.assertRaises(arff.BadLayout, self._load, r' "A\" ')

    def test_bad_quotes_sparse(self):
        self.assertRaises(arff.BadLayout, self._load, r" {0 \'A' }")
        self.assertRaises(arff.BadLayout, self._load, r" {0 \'A }")
        self.assertRaises(arff.BadLayout, self._load, " {0 'A }")
        self.assertRaises(arff.BadLayout, self._load, ' {0 "A }')
        self.assertRaises(arff.BadLayout, self._load, ' {0 A" }')
        self.assertRaises(arff.BadLayout, self._load, " {0 A' }")
        self.assertRaises(arff.BadLayout, self._load, r" {0 'A\' }")
        self.assertRaises(arff.BadLayout, self._load, r' {0 "A\" }')

    def test_multiple_values(self):
        self.assertRaises(arff.BadLayout, self._load, r" A B ")
        self.assertRaises(arff.BadLayout, self._load, r" 5 6 ")
        self.assertRaises(arff.BadLayout, self._load, r" '5' '6' ")

    def test_multiple_values_sparse(self):
        self.assertRaises(arff.BadLayout, self._load, r" {0 A B }")
        self.assertRaises(arff.BadLayout, self._load, r" {0 5 6 }")
        self.assertRaises(arff.BadLayout, self._load, r" {0 '5' '6' }")

    def test_internal_brace(self):
        self.assertRaises(arff.BadLayout, self._load, r" 0 {0 A }")
        self.assertRaises(arff.BadLayout, self._load, r" 0, {0 A }")
        self.assertRaises(arff.BadLayout, self._load, r" {0 A } 0")
        self.assertRaises(arff.BadLayout, self._load, r" {0 A }, 0")
        self.assertRaises(arff.BadLayout, self._load, r" {0")
        self.assertRaises(arff.BadLayout, self._load, r" 0}")

    # TODO: more tests of whitespace
    # TODO: tests escapes other than \", \' and \\
