import arff

import sys, getopt
from random import shuffle

def usage():
    u = 'arfftools [-s split_count] [-a arff_file]'
    print u
    
def main():
    
    splits = 0
    arff_filename = ''
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hs:a:')
    except getopt.GetoptError as err:
        #print str(err)
        usage()
        sys.exit(2)
        
    print optlist, args
    
    for opt, val in optlist:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt == '-s':
            splits = int(val)
        elif opt == '-a':
            arff_filename = val 
    
    print splits, arff_filename
    
    if not arff_filename:
        usage()
        sys.exit(2)
        
    fd = open(arff_filename,'r')
    data = arff.load(fd) 
    fd.close()
    print 'Data:', len(data['data'])
    arff_splits = arff.split(data,splits)
    for s in range(len(arff_splits)):
        filename_base = arff_filename.rsplit('.',1)[0]
        split_filename = '%s_split%d.arff' % (filename_base, s)
        fdsplit = open(split_filename, 'w')
        arff.dump(fdsplit, arff_splits[s])
        fdsplit.close()
        
if __name__ == '__main__':

    main()
