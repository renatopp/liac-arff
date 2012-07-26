# =============================================================================
# Federal University of Rio Grande do Sul (UFRGS)
# Connectionist Artificial Intelligence Laboratory (LIAC)
# Renato de Pontes Pereira - rppereira@inf.ufrgs.br
# =============================================================================
# Copyright (c) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
# =============================================================================

'''
The liac-arff module implements functions to read and write ARFF files in 
Python.
'''
__author__ = 'Renato de Pontes Pereira'
__author_email__ = 'renato.ppontes@gmail.com'
__version__ = '1.0'

import re
import csv

# Interal Helpers =============================================================
def __arff_to_str(s):
    '''Converts an ARFF value to a Python string'''
    s = s.strip('')
    if s.startswith('"') or s.startswith("'"):
        return s[1:-1]
    else:
        return s

def __str_to_arff(s):
    '''Converts a string to an ARFF value'''
    if s is None: s = '?'
    s = str(s)
    return "'%s'"%s if ' 'in s else s

def __decode_attribute(type_values):
    '''Eval the type/values of the attribute'''
    if type_values.upper() in ARFF_TYPES:
        type = type_values.upper()
        return (type, )
    else:
        values = next(csv.reader([type_values.strip('{} ')]))
        return ([v.strip(', \'"') for v in values], )

def __decode_values(values, attributes):
    '''Eval the values relative to attributes'''
    values = next(csv.reader([values.strip('{} ')]))
    values = [v.strip(', \'"') for v in values]

    result = []
    for attr, val in zip(attributes, values):
        type = attr[1]

        if val == '?': 
            value = None
        elif isinstance(type, (list, tuple)):
            value = val
        else:
            value = ARFF_TYPES[type](val)

        result.append(value)

    return result
# =============================================================================

# Constants ===================================================================
ARFF_TYPES = {
    'NUMERIC': float, 
    'REAL': float, 
    'INTEGER': int, 
    'STRING': __arff_to_str
}

COMMENT = '%'
RELATION = '@RELATION'
ATTRIBUTE = '@ATTRIBUTE'
DATA = '@DATA'
VALUE = 'VALUE'
# =============================================================================

class Reader(object):
    '''ARFF Reader'''

    def __init__(self, s):
        
        # A list of lines of ``s``
        self.__data = s.replace('\r', '').strip().split('\n')
        self.line_num = -1

    def __iter__(self):
        for line in self.__data:
            self.line_num += 1

            # Ignore empty lines
            line = line.strip()
            if not line: continue

            # Comments
            if line.startswith(COMMENT):
                yield (COMMENT, re.sub('^\%( )?', '', line))

            # Relation
            elif line.upper().startswith(RELATION):
                _, value = re.sub('( |\t)+', ' ', line).split(' ', 1)
                yield (RELATION, value)

            # Attributes
            elif line.upper().startswith(ATTRIBUTE):
                _, name, value = re.sub('( |\t)+', ' ', line).split(' ', 2)
                yield (ATTRIBUTE, name, value)

            # Data
            elif line.upper().startswith(DATA):
                yield (DATA,)

            # Data values
            else:
                yield (VALUE, line)

def loads(s): 
    '''Loads a string that contains an ARFF format structure'''
    reader = Reader(s)
    arff = {
        'description': u'',
        'relation': u'',
        'attributes': [],
        'data': []
    }

    last_token = None
    for line in reader:
        if line[0] == COMMENT and last_token is None:
            arff['description'] += line[1] + '\n'

        elif line[0] == RELATION:
            last_token = line[0]
            arff['relation'] = __arff_to_str(line[1])

        elif line[0] == ATTRIBUTE:
            last_token = line[0]
            arff['attributes'].append((__arff_to_str(line[1]),) + __decode_attribute(line[2]))

        elif line[0] == VALUE:
            last_token = line[0]
            arff['data'].append(__decode_values(line[1], arff['attributes']))

    return arff

def load(fp):
    '''Load an ARFF file'''
    return loads(fp.read())

class Writer(object):
    '''ARFF Writer'''

    def __init__(self):
        self.s = u''

    def write(self, *args):
        self.s += ' '.join(args)+'\n'

    def __str__(self):
        return str(self.s)

def dumps(obj):
    '''Returns a string in ARFF format from a given structure'''
    writer = Writer()

    # Description
    if 'description' in obj and obj['description']:
        for line in obj['description'].split('\n'):
            writer.write(COMMENT, line)

        writer.write()

    # Relation
    writer.write(RELATION, __str_to_arff(obj['relation']))
    writer.write()

    # Attributes
    for line in obj['attributes']:
        name = __str_to_arff(line[0])

        if not isinstance(line[1], (list, tuple)):
            type_values = __str_to_arff(line[1].upper())

        else:
            type_values = '{'+', '.join(
                [(__str_to_arff(i)) for i in line[1]]
            )+'}'

        writer.write(ATTRIBUTE, name, type_values)
    writer.write()

    # Data and data values
    writer.write(DATA)
    for line in obj['data']:
        writer.write(','.join([__str_to_arff(i) for i in line]))

    # Filler
    writer.write(COMMENT)
    writer.write(COMMENT)
    writer.write(COMMENT)

    return str(writer)

def dump(fp, obj):
    '''Write an ARFF file with the obj'''
    fp.write(dumps(obj))

if __name__ == '__main__':
    fp = open('C:\\Program Files (x86)\\weka-3-7\\data\\iris.arff')
    data = load(fp)
    import pprint
    pprint.pprint(data)
    print dumps(data)