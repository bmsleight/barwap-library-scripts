#!/bin/bash

SAMABALOCATION="/media/gallery-upload/"
LANDINGLOCATION="/home/bms/import/"
#SAMABALOCATION="/tmp/samba/"
#LANDINGLOCATION="/tmp/landing/"
# /usr/bin/flock -n /home/bms/importing.lock -c "/bin/bash /home/bms/barwap-library-scripts/library-import.sh"

#if [ "$(ls -A $DIR)" ]; then
if [ "$(find $SAMABALOCATION -maxdepth 0 -empty)" ]
then
  # No files to import so exit code 1
  # echo "No files" 
  exit 1
else
  # can Python not move accross filesystem bach can
  mv -f $SAMABALOCATION/* $LANDINGLOCATION
  /usr/bin/python  /home/bms/barwap-library-scripts/library-import.py
  if [ $? -eq 0 ]
  then
    # New files
    # echo "Run sigal"
    /usr/bin/python /usr/local/bin/sigal build -v -c /home/bms/barwap-library-scripts/sigal.conf.py /home/bms/orginals/ /home/bms/library.barwap.com/html/
    exit 0
  else
    # No files to import so exit code 1 
    # echo "No files Moved by library-import.py" 
    exit 1
  fi
fi






