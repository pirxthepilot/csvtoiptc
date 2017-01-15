#!/bin/bash
# Check tags

#BASEDIR='/var/run/media/joon/BYAHERO'
BASEDIR='/var/run/media/joon/BYAHERO/Byahero'

while read -r file; do
    file_base="$(basename "$file")"
    #if ! [[ "$file" =~ joon\/BYAHERO\/Byahero\/ ]] && ! [[ "$file" =~ \$RECYCLE ]] && ! [[ "$file" =~ \.Spotlight- ]] && ! [[ "$file_base" =~ ^\. ]] && ! [[ "$file_base" =~ ^Thumbs\.db ]]; then
    if ! [[ "$file" =~ \$RECYCLE ]] && ! [[ "$file" =~ \.Spotlight- ]] && ! [[ "$file_base" =~ ^\. ]] && ! [[ "$file_base" =~ ^Thumbs\.db ]] ; then
        printf "$file_base,"
        echo "$file"
    fi
done <<< "$( find "$BASEDIR" -type f )"

