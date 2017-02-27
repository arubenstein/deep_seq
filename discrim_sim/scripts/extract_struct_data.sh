#!/bin/bash

OUTPATH="/home/alizarub/git_repos/deep_seq/discrim_sim/results/"

rm -f $OUTPATH'/'structure_features.csv

echo "sequence,prot,pept,cst,amber" > $OUTPATH'/'structure_features.csv

for dir in $(find $OUTPATH -type d -name "???" | sort)
do
	cd $dir 
	echo $dir
	for filename in $(ls *.txt)
	do
		seq=${filename%.*}
		#taking out checking if amber ran properly - will just awk out the zero lines afterward.
	        #check_file $seq'_dat_binding'
        	#if [[ ! $? -eq 0 ]]; then
		#	continue
		#fi
		prot=$(awk '/#BEGIN/,/#END/ { if ($1 ~ /_(28|51|52|53|54|55|56|57|58|59|69|70|71|72|73|74|75|77|96|121|123|124|137|138|146|147|148|149|150|151|152|153|154|155|156|169|170|171|172|173|174|175|176|177|178|179|180|181|182|183|184|185)$/) {sum+=$NF} } END {print sum}' $seq'.txt') 
		pept=$(awk '/#BEGIN/,/#END/ { if ($1 ~ /_(19[7-9]|20[0-6])$/) {sum+=$NF} } END {print sum}' $seq'.txt')
		cst=$(tail -n 1 $seq'.txt' | awk '{print $2}')
		amber=$(cat $seq'_dat_binding')

		echo "$seq,$prot,$pept,$cst,$amber" >> $OUTPATH'/'structure_features.csv
	done
done

