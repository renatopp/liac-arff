__author__ = 'Hongjoo Lee'
__author_email__ = 'mamadontgodaddycomehome@gmail.com'

import unittest

import arff

class TestARFF(unittest.TestCase):
    def setUp(self):
        arff_text = \
'''
@relation software metric

@attribute number_of_files numeric
@attribute 'lines of code' numeric
@attribute defect density numeric

@data 10,10
'''
        self.__arff = arff.loads(arff_text)


    def test_space_can_be_included_in_the_attribute_name(self):
        attributes = self.__arff['attributes']
        self.assertEqual(attributes[0][0], 'number_of_files')
        self.assertEqual(attributes[1][0], 'lines of code')
        self.assertEqual(attributes[2][0], 'defect density')

    def test_space_can_be_included_in_the_relation_name(self):
        relation = self.__arff['relation']
        self.assertEqual(relation, 'software metric')

if __name__ == '__main__':
    unittest.main()
