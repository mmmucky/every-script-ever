#!/bin/bash
# A lightweight system to detect and sample changes of a file.

hash=`md5sum FILENAME | awk '{print $1}'`
while true; do
  new_hash=`md5sum FILENAME | awk '{print $1}'`
  if [ "$hash" == "$new_hash" ] ; then
    echo "file has not changed"
  else
    echo "file has changed"
    cp "FILENAME" "FILENAME.${new_hash}"
  fi
  sleep 0.01
  hash=$new_hash
done

