#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH
#
# Syntax: convert.py <csv file path>

import csv, sys
from subprocess import call

# Init
#

basedir = '/home/joon/Documents'

if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
skip_cols = ['Year', 'Folder location', 'Original filename', 'New filename']


# Main prog
#
with open(inputcsv, 'rb') as csvfile:
    csvdict = csv.DictReader(csvfile)
    for row in csvdict:
        exiftool_args = "" 
        for col,value in row.iteritems():
            if col in skip_cols:
                continue
            exiftool_args += col + ': "' + value + '" '
        print '========================='
        #print exiftool_args
        call(["echo", exiftool_args])
