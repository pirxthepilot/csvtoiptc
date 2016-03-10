#!/usr/bin/env python
#
# Syntax: file_check.py <csv file path>

import csv, sys, re, logging, os.path
#from subprocess import call

# Init
#

basedir = '/home/joon/Documents'
exiftool = '/usr/bin/exiftool'

logging.basicConfig(filename='file_check.log',level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
pathfix = re.compile(r"\./")
spacefix= re.compile(r"\s+")


# Main prog
#

logging.info('************************')
logging.info('***** STARTING RUN *****')
logging.info('************************')
logging.info('')
print '\n***** STARTING RUN *****\n'

with open(inputcsv, 'rb') as csvfile:
    csvdict = csv.DictReader(csvfile)

    for row in csvdict:
        
        filename = basedir + pathfix.sub('/', row['Original filename'])
        #filename = spacefix.sub(r"\ ", filename)

        #print filename

        if not os.path.isfile(filename):
            message = '  NOT FOUND: ' + filename
            logging.error(message)
            print message

# Done!
logging.info('')
logging.info('+++++ RUN COMPLETE +++++')
print '\n+++++ RUN COMPLETE +++++\n'
