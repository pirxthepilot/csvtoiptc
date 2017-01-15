#!/usr/bin/env python
#
# Syntax: file_check.py <csv file path>

import csv, sys, re, logging, os

# Init
#

basedir = '/run/media/joon/GSV Sleeper Service/Byahero'
#basedir = '/home/joon/Documents'

logging.basicConfig(filename='rename.log',level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: rename.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
pathfix = re.compile(r"\./")
spacefix= re.compile(r"\s+")
sdyear = re.compile(r"^\d{4}$")
src_field = 'Original filename'
dst_field = 'New filename'

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

        source = basedir + pathfix.sub('/', row[src_field])
        subdir = source.split('/')
        subappend = ''

        for i in range(-2,-6,-1):
            if subappend != '':
                subappend = subdir[i] + '/' + subappend
            else:
                subappend = subdir[i]
            if sdyear.match(subdir[i]):
                destination = basedir + '/' + subappend + '/' + row[dst_field]
                break

        print 'Original file: %s' % source
        print 'New file: %s' % destination

        if not os.path.isfile(source):
            message = '  NOT FOUND: ' + source
            logging.error(message)
            print message
            continue

        if source == destination:
            message = "Source and destination are similar. Skipping.."
            logging.info(message)
            print message
            continue

        # Rename proper
        try:
            os.rename(source, destination)
        except Exception as e:
            logging.error('Error: %s') %e.message

# Done!
logging.info('')
logging.info('+++++ RUN COMPLETE +++++')
print '\n+++++ RUN COMPLETE +++++\n'
