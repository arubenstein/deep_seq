#!/bin/bash

#must test that fitnesses change doesn't make a diff

csv=$1
n_sample=$2

bn=$(basename $csv .csv)
name=${bn:8}

if [[ $n_sample -eq 2 ]]
then
	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" && $8 >= $11 {print $1,0.0,$8} ' $csv > $name'_uncleaved_fitness_ratio.csv' #$8+$11/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" && $8 < $11 {print $1,0.0,$11} ' $csv >> $name'_uncleaved_fitness_ratio.csv' #$8+$11/2

	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" && $14 >= $17 {print $1,1.0,$14} ' $csv > $name'_cleaved_fitness_ratio.csv' #$14+$17/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" && $14 < $17 {print $1,1.0,$17} ' $csv >> $name'_cleaved_fitness_ratio.csv' #$14+$17/2

	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" && $2 >= $5 {print $1,0.5,$2} ' $csv > $name'_middle_fitness_ratio.csv' #$2+$5/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" && $2 < $5 {print $1,0.5,$5} ' $csv >> $name'_middle_fitness_ratio.csv' #$2+$5/2

else
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" {print $1,0.0,$5} ' $csv > $name'_uncleaved_fitness_ratio.csv'
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" {print $1,1.0,$8} ' $csv > $name'_cleaved_fitness_ratio.csv'
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" {print $1,0.5,$2} ' $csv > $name'_middle_fitness_ratio.csv'
fi
 
