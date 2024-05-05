#!/bin/bash

SAMABALOCATION="/home/bms/nextcloud-files/photos/files/"
LANDINGLOCATION="/home/bms/import/"
#SAMABALOCATION="/tmp/samba/"
#LANDINGLOCATION="/tmp/landing/"
# /usr/bin/flock -n /tmp/importing.lock -c "/bin/bash /home/bms/barwap-library-scripts/library-import.sh"

#if [ "$(ls -A $DIR)" ]; then
if [ "$(find $SAMABALOCATION -maxdepth 0 -empty)" ]
then
  # No files to import so exit code 1
  echo "No files" 
  exit 1
else
  # If empty gets removed
  mkdir $LANDINGLOCATION
  # move them form Nextcloud to landing location
  mv -f $SAMABALOCATION/* $LANDINGLOCATION
  sudo nextcloud.occ files:scan photos
  /usr/bin/python3  /home/bms/barwap-library-scripts/library-import.py >/tmp/li.log 2>&1
  if [ $? -eq 0 ]
  then
    # New files
    # echo "Run sigal"
    /usr/bin/python3 /usr/local/bin/sigal build -v -c /home/bms/barwap-library-scripts/sigal.conf.py /home/bms/orginals/ /home/bms/library.barwap.com/html/
    exit 0
  else
    # No files to import so exit code 1 
    echo "No files Moved by library-import.py" 
    exit 1
  fi
fi







