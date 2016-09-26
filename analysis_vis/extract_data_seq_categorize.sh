#!/bin/bash

csv=$1

bn=$(basename $csv .csv)
name=${bn:8}

awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" {print $1,0} ' $csv > $name'_uncleaved_fitness.csv'
awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" {print $1,1} ' $csv > $name'_cleaved_fitness.csv'
awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" {print $1,0.5} ' $csv > $name'_middle_fitness.csv' 
