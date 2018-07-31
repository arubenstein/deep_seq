#!/bin/bash

path=$1
actual_fn=$2
outpath=$3
server=$4

pattern="*.OrientFrags.fasta"
pattern_input_fast="*.extendedFrags*.fasta"
       
cd $path

ls ''$pattern'' > $actual_fn'_files_list.txt'

cat $(grep -v '^#' $actual_fn'_files_list.txt' ) > $outpath'/'$actual_fn'.fasta'

python $SCRIPTS'/cut_c.py' --infile $outpath'/'$actual_fn'.fasta' --outpath $outpath

perl $SCRIPTS'/fasta2FakeFastq.pl' $outpath'/'$actual_fn'_cut.fasta' > $outpath'/'$actual_fn'_cut.fastq'

input_n_seq=$(grep ">" ''$pattern_input_fast'' | wc -l | awk 'END {print $1}')
beg_n_seq=$(grep ">" ''$pattern'' | wc -l | awk 'END {print $1}')
end_n_seq=$(grep "@" $outpath'/'$actual_fn'_cut.fastq' | wc -l | awk 'END {print $1}')
nomatch_n_seq=$(grep ">" $outpath'/'$actual_fn'_nomatch.fasta' | wc -l | awk 'END {print $1}')
dummy_n_seq=$(grep ">dummy" $outpath'/'$actual_fn'.fasta' | wc -l | awk 'END {print $1}')

full_n_seq=$((end_n_seq + nomatch_n_seq + dummy_n_seq))

if [ $full_n_seq -eq $beg_n_seq ] && [ $full_n_seq -eq $input_n_seq ]
then
	echo "Success in processing $beg_n_seq sequences"
else
	echo "Error in processing $beg_n_seq sequences"
fi

echo "Input: $input_n_seq sequences"
echo "Initial: $beg_n_seq sequences"
echo "Final: $end_n_seq sequences"
echo "No Align: $nomatch_n_seq sequences"
echo "Dummy: $dummy_n_seq sequences"
