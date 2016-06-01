#!/bin/bash

path=$1
list_dirs=$2
output_path=$3
pattern=$4

cd $path

rm -rf $output_path'/'*

while read dir
do

        

	cd $dir
	cd Amplicon1/data/output/

        for filename in $(ls $pattern )
        do
		if [[ $filename =~ "DNA" ]]
		then
			class="DNA"
		else 
			class="PRO"
		fi

		if [[ $filename =~ "m1" ]]
		then
			nmut="m1"
		elif [[ $filename =~ "m2" ]]
		then
			nmut="m2"
		else
			nmut="all"
		fi

		if [[ "$class" == "DNA" ]]
		then
			WT="GATGAAATGGAAGAA"
		else
			WT="DEMEE"
		fi

                mkdir -p $output_path'/'$class'_'$nmut'/'

		if [[ "$pattern" =~ "ratios" ]]
		then
			actual_fn=$(echo $filename | awk -F'Sample' '{printf "Sample"substr($2,1,1)"_Sample"substr($3,1,1)}')
	                awk ' $NF ~ /[0-9]/ {print $8}' $filename > $output_path'/'$class'_'$nmut'/'$actual_fn
	                WT_count=$(awk -v w=$WT ' $2 == w {print $8}' $filename )		
		else
			actual_fn=$(echo $filename | awk -F'_' '{print $2}')
	                awk ' $NF ~ /[0-9]/ {print $NF}' $filename > $output_path'/'$class'_'$nmut'/'$actual_fn
	                WT_count=$(awk -v w=$WT ' $2 == w {print $NF}' $filename )
		fi
		
	
		if [ ! -z "$WT_count" ]
		then
			echo $actual_fn " " $WT_count >> $output_path'/'$class'_'$nmut'/'wild_type_counts
		fi

		touch $output_path'/'$class'_'$nmut'/'wild_type_counts
	done

        cd $path 

done < $list_dirs

for wild_type in $(find $output_path'/'*'/'wild_type_counts)
do
	sort $wild_type | uniq > $wild_type'.txt'
done
