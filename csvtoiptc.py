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
import time

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

def log(message, type='info'):
    if type == 'info':
        logging.info(message)
    elif type == 'error':
        logging.error(message)
    print "%s" % message

def find(name, path):
    for root, dirs, files in os.walk(path):
        for fn in files:
            if name.lower() == fn.lower():
                return os.path.join(root, fn)


# Init
#

exiftool = '/usr/bin/exiftool'

logging.basicConfig(filename='keywordtags.log', level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: csvtoiptc.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])


# Main prog
#

log('***** STARTING RUN *****')
log('')

# Declarations
filelist = {}
filenotfound = False

# Preprocess files
log('Checking files...')
with open(inputcsv, 'rb') as csvfile:
    csvdict = csv.DictReader(csvfile)
    for row in csvdict:
        # Do not process blank lines
        if not row['Original filename']:
            continue
        # Find file and get full relative path
        filename = find("%s.%s" % (row['Original filename'], row['File Type']), '.')
        if not filename:
            log("  '%s' not found!" % row['Original filename'], 'error')
            filenotfound = True
            continue
        if not os.path.isfile(filename):
            log("  %s not found!" % filename, 'error')
            filenotfound = True
            continue
        filelist[filename] = row

# Exit if there are missing files
if filenotfound:
    log('One or more files in the csv not found! Exiting.', 'error')
    sys.exit()
else:
    log('No missing files - great! Processing %s files.' % len(filelist))
    log('')

#print filelist
#sys.exit()

# Run loop
count = 0
for filename, row in filelist.iteritems():

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
    #time.sleep(2)

    # Run!
    count += 1
    log('===================')
    log('[%s]' % count)
    log('PROCESSING ' + filename)

    p = subprocess.Popen(exiftool_cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if stdout:
        log(stdout)
    if stderr:
        log(stderr, 'error')

# Done!
log('')
log('+++++ RUN COMPLETE (%s files processed) +++++' % len(filelist))
