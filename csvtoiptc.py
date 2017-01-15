#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH
#
# Syntax: csvtoiptc.py <csv file path>

import csv
import sys
import re
import logging
import subprocess
import os

# CSV-IPTC mappings
#
iptcfromcsv = {
    'Country':     'Country',
    'Description': 'Short Description',
    'Keywords':    'Keywords',
    'Subject':     'Keywords',
}


# Functions
#

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Init
#

exiftool = '/usr/bin/exiftool'

logging.basicConfig(filename='keywordtags.log', level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])


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

        # Find file and get full relative path
        filename = find("%s.%s" % (row['Original filename'], row['File Type'].lower()), '.')

        if not os.path.isfile(filename):
            print "%s not found!" % filename
            continue

        # Call exiftool
        exiftool_cmd = ['/usr/bin/exiftool', '-overwrite_original', '-sep', '; ']

        # Set tag args
        for iptcparam, csvparam in iptcfromcsv.iteritems():
            if row[csvparam] == "":
                continue
            # If tag is a list, do something special
            # if ";" in value:
            #     taglist = value.split("; ")
            #     for tagval in taglist:
            #         exiftool_cmd.append('-' + tag + '=' + tagval)
            # else:
            exiftool_cmd.append('-' + iptcparam + '=' + row[csvparam])


        # Filename
        exiftool_cmd.append(filename)
        #print exiftool_cmd

        # Run!
        logging.info('===================\n')
        logging.info('PROCESSING ' + filename)
        print '================'
        count += 1
        print '[%s]' % count
        print 'PROCESSING ' + filename
        #print exiftool_cmd

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
