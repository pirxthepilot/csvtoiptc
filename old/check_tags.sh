#!/bin/bash
# Check tags

BASEDIR='/var/run/media/joon/BYAHERO/Byahero'

while read -r file; do
    if [[ $file =~ \.(mov|mp4|m4v|wmv|mpg|m2p|flv|avi)$ ]]; then
        printf "$(basename "$file"),"
        echo "\"$( exiftool -Description "$file" 2>/dev/null | awk -F ": " '{ print $2 }' )\""
    fi
done <<< "$( find "$BASEDIR" -type f )"

