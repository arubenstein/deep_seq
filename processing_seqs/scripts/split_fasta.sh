#!/bin/bash

file=$1
actual_fn=$2 
outpath=$3
server=$4

cd $outpath

#-f - output file name
#--seqs_per_file is self-explanatory 
perl $SCRIPTS'/split_multifasta.pl' --in $file  --output_dir=$outpath --f=$actual_fn --seqs_per_file=10000


