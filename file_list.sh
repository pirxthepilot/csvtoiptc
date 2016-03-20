#!/bin/bash
# Check tags

BASEDIR='/var/run/media/joon/GSV Sleeper Service/Byahero'

while read -r file; do
    printf "$(basename "$file"),"
    echo "$file"
done <<< "$( find "$BASEDIR" -type f )"

