#!/bin/bash

source=$1
dest=$2

curr=$(date +%s)

while /bin/true; do
  latest=$(date +%s)
  diff=$(( latest - curr ))
  if [ $diff -ge 82800 ]; then #23 hours = 82800 seconds
    rsync -av $source'/'* $dest #just in case, transfer everything a bit early

    sleep 35m

    rsync -av $source'/'* $dest #one last transfer, hopefully before job is killed     

    exit

  else
    sleep 60m
  fi

done
