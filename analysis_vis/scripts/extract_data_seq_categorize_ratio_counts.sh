#!/bin/bash

#must test that fitnesses change doesn't make a diff

csv=$1
n_sample=$2

bn=$(basename $csv .csv)
name=${bn:8}

if [[ $n_sample -eq 2 ]]
then
	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" && $8 >= $11 {print $1,0.0,$8,$9,$10} ' $csv > $name'_uncleaved_fitness_ratio_count.csv' #$8+$11/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" && $8 < $11 {print $1,0.0,$11,$12,$13} ' $csv >> $name'_uncleaved_fitness_ratio_count.csv' #$8+$11/2

	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" && $14 >= $17 {print $1,1.0,$14,$15,$16} ' $csv > $name'_cleaved_fitness_ratio_count.csv' #$14+$17/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" && $14 < $17 {print $1,1.0,$17,$18,$19} ' $csv >> $name'_cleaved_fitness_ratio_count.csv' #$14+$17/2

	awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" && $2 >= $5 {print $1,0.5,$2,$3,$4} ' $csv > $name'_middle_fitness_ratio_count.csv' #$2+$5/2
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" && $2 < $5 {print $1,0.5,$5,$6,$7} ' $csv >> $name'_middle_fitness_ratio_count.csv' #$2+$5/2

else
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-4) != "" {print $1,0.0,$5,$6,$7} ' $csv > $name'_uncleaved_fitness_ratio_count.csv'
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-3) != "" {print $1,1.0,$8,$9,$10} ' $csv > $name'_cleaved_fitness_ratio_count.csv'
        awk -F, 'BEGIN{OFS=","} NR != 1 && $(NF-2) != "" {print $1,0.5,$2,$3,$4} ' $csv > $name'_middle_fitness_ratio_count.csv'
fi
 
