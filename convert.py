#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH
#
# Syntax: convert.py <csv file path>

import csv, sys, re
from subprocess import call

# Init
#

basedir = '/home/joon/Documents'
exiftool = '/usr/bin/exiftool'

if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
skip_cols = ['Year', 'Folder location', 'Original filename', 'New filename', 'CopyrightStatus']
pathfix = re.compile(r"\./")
spacefix= re.compile(r"\s+")


# Main prog
#
with open(inputcsv, 'rb') as csvfile:
    csvdict = csv.DictReader(csvfile)

    for row in csvdict:
        
        # File path fixes
        filename = basedir + pathfix.sub('/', row['Original filename'])
        #filename = spacefix.sub(r"\ ", filename)
        
        # Call exiftool
        exiftool_cmd = [ '/usr/bin/exiftool' ] 

        # Prep some tags
        if row['CopyrightStatus'].lower() == 'copyrighted':
            #row['xmpRights:Marked'] = 'True'
            row['Marked'] = 'True'
        else:
            #row['xmpRights:Marked'] = 'False'
            row['Marked'] = 'False'

        # Set tag args
        for tag,value in row.iteritems():
            if tag in skip_cols:
                continue
            if value == "":
                continue
            #exiftool_cmd.append('-' + tag + '="' + value + '"')
            exiftool_cmd.append('-' + tag + '=' + value)
        
        # Filename
        exiftool_cmd.append(filename)

        # Run!
        print '================'
        print 'Processing ' + filename
        #print exiftool_cmd
        call(exiftool_cmd)
