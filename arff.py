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
import sys

import random


if 'unicode' not in __builtins__:
    # if `unicode` is not defined, we run in a python3 enviroment where all
    # string literals are unicode, so we don't need to convert it to one.
    # if `s` is not a string, we need to convert it...
    def unicode(s):
        if isinstance(s, str):
            return s
        return str(s)


# Interal Helpers =============================================================

#Exceptions
class WrongTypeException(Exception):
    pass

def __arff_to_str(s):
    '''Converts an ARFF value to a Python string'''
    s = s.strip(u'')
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace(r'\"', '"')
    elif s.startswith("'") and s.endswith("'"):
        return s[1:-1].replace(r"\'", "'")
    else:
        return s

def __str_to_arff(s):
    '''Converts a string to an ARFF value'''
    if s is None: s = '?'
    s = unicode(s)
    return u"'%s'" % s.replace("\\", r"\\").replace("'", r"\'").replace("\n", ' ').replace("\r", ' ')

def __check_nominal(values, s):
    assert s in values, "%s was not listed as a valid nominal value" % s
    return s

def __check_nominal_factory(values):
    return lambda x: __check_nominal(values, x)

def __encode_attribute(type_values):
    '''create encoding functions for the attribute'''
    if isinstance(type_values, (list, tuple)):
        values = type_values
        return __check_nominal_factory(values)
    elif type_values.upper() in ENCODE_ARFF_TYPES:
        type = ENCODE_ARFF_TYPES[type_values.upper()]
        return type
    else:
        raise ValueError("%s is not of a supported attribute type" % type_values)

def __encode_values(values, attributes):
    '''
        Encode the values relative to their attributes.
    attributes is a list of tuples with the arff type and the conversion function.
    e.g. [('REAL',<type 'float'>)]
    '''
    result = []
    for attr_func, val in zip(attributes, values):
        if val is None:
            result.append( '?' )
        else:
            try:
                result.append(unicode(attr_func[1](val)))
            except AssertionError as e:
                raise AssertionError( "\n".join( [str(e), "Values:", str(values) ] ) )
            except ValueError as e:
                # pass as argument to the exeption the value,
                #the arff type, and the list of values
                raise WrongTypeException(val, attr_func[0], str(values))

    return result

def __decode_attribute(type_values):
    '''Eval the type/values of the attribute'''
    if type_values.upper() in DECODE_ARFF_TYPES:
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
            if not val:
                val = '0'
            value = DECODE_ARFF_TYPES[type](val)

        result.append(value)

    return result
# =============================================================================

# Constants ===================================================================
ENCODE_ARFF_TYPES = {
    'NUMERIC': float,
    'REAL': float,
    'INTEGER': int,
    'STRING': __str_to_arff
}
DECODE_ARFF_TYPES = {
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
                _, name, value = line.partition(' '.join(re.sub('( |\t)+', ' ', line).split(' ')[1:-1]))
                yield (ATTRIBUTE, name, value)

            # Data
            elif line.upper().startswith(DATA):
                yield (DATA,)

            # Data values
            else:
                yield (VALUE, line)


def split(arff, n):
    ''' Randomly splits ARFF data into n parts'''
    arff_splits = []
    splits = [[] for i in range(n)]
    print "Splits", len(splits)
    data = arff['data']
    random.shuffle(data)
    print "Data length", len(data)
    for d in range(len(data)):
        splits[d % n].append(data[d])
    for split in splits:
        arff_split = {
            'description': arff['description'],
            'relation': arff['relation'],
            'attributes': arff['attributes'],
            'data': split
        }
        #print "Split length", len(split)
        arff_splits.append(arff_split)
    return arff_splits

def loads(s):
    '''Loads a string that contains an ARFF format structure'''
    reader = Reader(s.decode('utf-8'))
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

class StringWriter(object):
    '''ARFF String Writer'''

    def __init__(self):
        self.lines = []

    def write(self, *args):
        self.lines += [u' '.join(args)]

    def __str__(self):
        return str('\n'.join(self.lines))

    def __unicode__(self):
        return unicode('\n'.join(self.lines))


class ARFFWriter(object):
    '''ARFF File Writer'''

    def __init__(self, f):
        self.f = f

    def write(self, *args):
        self.f.write(u' '.join(args) + '\n')

def dump_to_writer(writer, obj):
    # Description
    if 'description' in obj and obj['description']:
        for line in obj['description'].split('\n'):
            writer.write(COMMENT, line)

        writer.write()

    # Relation
    writer.write(RELATION, __str_to_arff(obj['relation']))
    writer.write()

    # Attributes
    data_funcs = []
    for line in obj['attributes']:
        name = __str_to_arff(line[0])

        if not isinstance(line[1], (list, tuple)):
            type_values = __str_to_arff(line[1].upper())

        else:
            type_values = '{'+', '.join(
                [(__str_to_arff(i)) for i in line[1]]
            )+'}'

        writer.write(ATTRIBUTE, name, type_values)
        #append a tuple with the srff type and the python coversion function
        data_funcs.append( (line[1], __encode_attribute( line[1] )) )
    writer.write()

    # Data and data values
    writer.write(DATA)
    for line in obj['data']:
        writer.write(u','.join(__encode_values(line, data_funcs)))

    # Filler
    writer.write(COMMENT)
    writer.write(COMMENT)
    writer.write(COMMENT)

def dumps(obj):
    '''Returns a string in ARFF format from a given structure'''

    writer = StringWriter()
    dump_to_writer(writer, obj)

    return unicode(writer)

def dump(fp, obj):
    '''Write an ARFF file with the obj'''
    writer = ARFFWriter(fp)
    dump_to_writer(writer, obj)
