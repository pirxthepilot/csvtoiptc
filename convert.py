#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH
#
# Syntax: convert.py <csv file path>

import csv, sys, re, logging, subprocess
#from subprocess import call

# Init
#

basedir = '/run/media/joon/GSV Sleeper Service/Byahero'
exiftool = '/usr/bin/exiftool'

logging.basicConfig(filename='csvtoiptc.log',level=logging.DEBUG)
logging.info('\n\n\n')


if len(sys.argv) != 2:
    print "Syntax: convert.py <csv file path>"
    sys.exit()

inputcsv = str(sys.argv[1])
skip_cols = ['Year', 'Folder location', 'Original filename', 'New filename', 'CopyrightStatus']
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

    count = 0

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
            #print exiftool_cmd
        
        # Filename
        exiftool_cmd.append(filename)

        # Run!
        logging.info('===================\n')
        logging.info('PROCESSING ' + filename)
        print '================'
        count += 1
        print '[%s]' % count
        print 'PROCESSING ' + filename
        #print exiftool_cmd

        p = subprocess.Popen(exiftool_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
