#!/bin/bash
# Check tags

BASEDIR='/var/run/media/joon/GSV Sleeper Service/Byahero'

while read -r file; do
    if [[ $file =~ \.(mov|mp4|m4v|wmv|mpg|m2p|flv|avi)$ ]]; then
        printf "$(basename "$file"),"
        echo "\"$( exiftool -SubjectCode "$file" | awk -F ": " '{ print $2 }' )\""
    fi
done <<< "$( find "$BASEDIR" -type f )"

#shit=$( find "$BASEDIR" -type f )
#echo "$shit"
