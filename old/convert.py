#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH
#
# Syntax: convert.py <csv file path>

import csv
import sys
import re
import logging
import subprocess
import os


# Init
#

basedir = '/run/media/joon/GSV Sleeper Service/Byahero'
# basedir = '/home/joon/Documents'
exiftool = '/usr/bin/exiftool'

logging.basicConfig(filename='keywordtags.log', level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
skip_cols = ['Year', 'Folder location', 'Original filename',
             'New filename', 'CopyrightStatus']
pathfix = re.compile(r"\./")


# Main prog
#

logging.info('************************')
logging.info('***** STARTING RUN *****')
logging.info('************************')
logging.info('')
print '\n***** STARTING RUN *****\n'

with open(inputcsv, 'rb') as csvfile:
    csvdict = csv.DictReader(csvfile)

    count = 0

    for row in csvdict:

        # File path fixes
        filename = basedir + pathfix.sub('/', row['Original filename'])
        filename = os.path.dirname(os.path.abspath(filename)) + '/' + row['New filename']

        # if not os.path.isfile(filename):
        #    continue

        # Call exiftool
        exiftool_cmd = ['/usr/bin/exiftool', '-overwrite_original', '-sep', '; ']

        # Prep some tags
        # if row['CopyrightStatus'].lower() == 'copyrighted':
        #     row['Marked'] = 'True'
        # else:
        #     row['Marked'] = 'False'

        # Set tag args
        for tag, value in row.iteritems():
            if tag in skip_cols:
                continue
            if value == "":
                continue
            # If tag is a list, do something special
            # if ";" in value:
            #     taglist = value.split("; ")
            #     for tagval in taglist:
            #         exiftool_cmd.append('-' + tag + '=' + tagval)
            # else:
            exiftool_cmd.append('-' + tag + '=' + value)

            # print exiftool_cmd

        # Filename
        exiftool_cmd.append(filename)

        # Run!
        logging.info('===================\n')
        logging.info('PROCESSING ' + filename)
        print '================'
        count += 1
        print '[%s]' % count
        print 'PROCESSING ' + filename
        # print exiftool_cmd

        p = subprocess.Popen(exiftool_cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        if stdout:
            logging.info(stdout)
            print stdout
        if stderr:
            logging.error(stderr)
            print stderr

# Done!
logging.info('')
logging.info('+++++ RUN COMPLETE +++++')
print '\n++++ RUN COMPLETE +++++\n'
