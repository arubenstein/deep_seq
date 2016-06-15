#!/bin/bash

fasta=$1
actual_fn=$2
outpath=$3
server=$4

cd $outpath

python $SCRIPTS'/cut_c.py' --infile $fasta --outpath $outpath --nextseq True

perl $SCRIPTS'/fasta2FakeFastq.pl' $outpath'/'$actual_fn'_cut.fasta' > $outpath'/'$actual_fn'_cut.fastq'

beg_n_seq=$(grep ">" $fasta | wc -l | awk 'END {print $1}')
end_n_seq=$(grep "@" $outpath'/'$actual_fn'_cut.fastq' | wc -l | awk 'END {print $1}')
nomatch_n_seq=$(grep ">" $outpath'/'$actual_fn'_nomatch.fasta' | wc -l | awk 'END {print $1}')
dummy_n_seq=$(grep ">dummy" $fasta | wc -l | awk 'END {print $1}')

full_n_seq=$((end_n_seq + nomatch_n_seq + dummy_n_seq))

if [ $full_n_seq -eq $beg_n_seq ] 
then
	echo "Success in processing $beg_n_seq sequences"
else
	echo "Error in processing $beg_n_seq sequences"
fi

echo "Initial: $beg_n_seq sequences"
echo "Final: $end_n_seq sequences"
echo "No Align: $nomatch_n_seq sequences"
echo "Dummy: $dummy_n_seq sequences"
