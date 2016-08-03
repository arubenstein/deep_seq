#!/bin/bash

csv=$1

bn=$(basename $csv .csv)
name=${bn:9}

awk -F, ' NR != 1 && $(NF-4) != "" {print $1} ' $csv > $name'_uncleaved.txt'
awk -F, ' NR != 1 && $(NF-3) != "" {print $1} ' $csv > $name'_cleaved.txt'
awk -F, ' NR != 1 && $(NF-2) != "" {print $1} ' $csv > $name'_middle.txt' 
