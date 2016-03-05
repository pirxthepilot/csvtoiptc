#!/usr/bin/env python
# Whaddya say we do this in python ey?
# HELLZ YEAH

import csv
from subprocess import call

basedir = '/home/joon/Documents'

with open('sample.csv', 'rb') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
      print row['one'] + ' ' + row['three'] + ': '+ row['two']

call(["ls", "-l", basedir + '/2015'])
