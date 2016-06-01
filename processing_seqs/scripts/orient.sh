#!/bin/bash

file=$1
actual_fn=$2 
outpath=$3
server=$4

cd $outpath

extension="${actual_fn##*.extendedFrags}"
filename="${actual_fn%.*}"

prefix=$filename'_'$extension

mkdir -p $filename
cd $filename

dummy=">dummy
GTTCCAGACTACGCTCTGCAGGCTAGTGGTGGAGGAGGCTCTGGTGGAGGCGGTAGCGGA
GGCGGAGGGTCGCTTCAGCCTTTGCCTTGTGCTTCTCATTTGGGCAGTGATTATAAAGAT
GATGATGATAAAGGCAGTG"

echo "$dummy" | cat - $file > $actual_fn.fasta

nohup nice perl $SCRIPTS'/seqorient.pl' -r 1 $actual_fn.fasta > $prefix.OrientFrags.fasta 2>> $prefix.OrientFrags.log
