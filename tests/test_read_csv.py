import unittest

import arff

class TestReadCSV(unittest.TestCase):
    def test_quotation_marks(self):
        fixture = """'A,B'"""
        expected = ["""'A,B'"""]
        v = arff._read_csv(fixture)
        self.assertEqual(v, expected)

        fixture_2 = '''"A,B"'''
        expected_2 = ['''"A,B"''']
        v = arff._read_csv(fixture_2)
        self.assertEqual(v, expected_2)

        fixture_3 = ''' 'A','B','A,B' '''
        expected_3 = [""" 'A'""", """'B'""", """'A,B' """]
        v = arff._read_csv(fixture_3)
        self.assertEqual(v, expected_3)

        fixture_4 = ''' '"' '''
        expected_4 = [""" '"' """]
        v = arff._read_csv(fixture_4)
        self.assertEqual(v, expected_4)

    def test_open_quotation_marks(self):
        fixture = """ 'A """
        self.assertRaisesRegexp(
            ValueError,
            """Quote not closed for line:  'A""",
            arff._read_csv,
            fixture
        )

    def test_regular_csv(self):
        fixture = 'sunny,85.0,85.0,FALSE,no'
        expected = ['sunny', '85.0', '85.0', 'FALSE', 'no']

        v = arff._read_csv(fixture)
        self.assertEqual(v, expected)

    def test_escape_characters(self):
        fixture = """\"\\\\\""""
        expected = ["""\"\\\\\""""]

        v = arff._read_csv(fixture)
        self.assertEqual(v, expected)

        fixture = """\"\\\\,\",\",\\\\\""""
        expected = ["""\"\\\\,\"""", """\",\\\\\""""]

        v = arff._read_csv(fixture)
        self.assertEqual(v, expected)

    def test_ill_quoted(self):
        fixture = "a'"

        with self.assertRaisesRegexp(ValueError,
                                     "Quote not closed for line: a'"):
            arff._read_csv(fixture)
