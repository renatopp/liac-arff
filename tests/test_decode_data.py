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
        print(txt)
        return arff.load(txt)['data']

    def test_quotes(self):
        result = self._load("""'ENACT.NOGOPMAJ,2017'""")
        self.assertListEqual(result, [['ENACT.NOGOPMAJ,2017']])

        result = self._load('''"ENACT.NOGOPMAJ,2017"''')
        self.assertListEqual(result, [['ENACT.NOGOPMAJ,2017']])

        result = self._load(''' 'A','B' , '"','C,D' ''', 4)
        self.assertListEqual(result, [['A', 'B', '"', 'C,D']])

    def test_quotes_sparse(self):
        result = self._load("""{0 'ENACT.NOGOPMAJ,2017'}""")
        self.assertListEqual(result, [['ENACT.NOGOPMAJ,2017']])

        result = self._load('''{0 "ENACT.NOGOPMAJ,2017"}''')
        self.assertListEqual(result, [['ENACT.NOGOPMAJ,2017']])

        result = self._load('''{ 0 'A',1 'B' ,2 '"',3 'C,D' }''', 4)
        self.assertListEqual(result, [['A', 'B', '"', 'C,D']])

    def test_escapes(self):
        result = self._load(r''' '\'' ''')
        self.assertListEqual(result, [["'"]])
        result = self._load(r''' '\\' ''')
        self.assertListEqual(result, [["\\"]])
        result = self._load(r''' '\\\'' ''')
        self.assertListEqual(result, [["\\'"]])

    def test_escapes_sparse(self):
        result = self._load(r''' {0 '\''} ''')
        self.assertListEqual(result, [["'"]])
        result = self._load(r''' {0 '\\'} ''')
        self.assertListEqual(result, [["\\"]])
        result = self._load(r''' {0 '\\\''} ''')
        self.assertListEqual(result, [["\\'"]])

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

    # TODO: more tests of whitespace
    # TODO: tests escapes other than \", \' and \\
