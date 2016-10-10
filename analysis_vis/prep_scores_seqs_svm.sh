#!/bin/bash

path=~/git_repos/deep_seq/analysis_vis/seq_lists_shiryaev/
conversion_type=$1

for seq_list in $(ls $path*.txt)
do

    if [[ ! $seq_list =~ "list3M5L" ]]
    then
        continue
    fi

    if [[ $seq_list =~ "uncleaved" ]]
    then
        label="UNCLEAVED"
    elif [[ $seq_list =~ "cleaved" ]]
    then
        label="CLEAVED"
    else
        label="MIDDLE"
    fi

    base=$(basename $seq_list '.txt')
    echo $base
    grep -f $seq_list $path'structure_features.csv' | sort > $path$base'_structure_features.csv'
    awk -F, '{print $1}' $path$base'_structure_features.csv' > $path$base'_seqs_data.list' 
    grep -f $path$base'_seqs_data.list' $path$base'_structure_features.csv' | awk -F, -v l=$label 'BEGIN{OFS=","}; {for (i=2; i<=NF; i++) printf $i","}{print l}' > $path$base'_struct.csv'
    grep -f $path$base'_seqs_data.list' $path$base'_sequence_features_'$conversion_type'.csv' | awk -F, -v l=$label 'BEGIN{OFS=","}; {for (i=2; i<=NF; i++) printf $i","}{print l}'  > $path$base'_seq_'$conversion_type'.csv'
    awk -F, -v l=$label 'BEGIN{OFS=","}; {printf $1} {for ( i=2; i<NF; i++) printf ","$i} {printf ",\n"}' $path$base'_seq_'$conversion_type'.csv' > $path$base'_seq_'$conversion_type'_nolabel.csv'
    paste -d'\0' $path$base'_seq_'$conversion_type'_nolabel.csv' $path$base'_struct.csv' > $path$base'_structseq_'$conversion_type'.csv'
     
done

while read line
do
    l=$(echo $line | awk -F, '{print $1}')
    c=$(echo $line | awk -F, '{print $2}')
    u=$(echo $line | awk -F, '{print $3}')

    cat $path$c'_struct.csv' $path$u'_struct.csv' > $path$l"_struct.csv"
    cat $path$c'_seq.csv' $path$u'_seq.csv' > $path$l"_seq.csv"
    cat $path$c'_structseq.csv' $path$u'_structseq.csv' > $path$l"_structseq.csv"

done < $path'/cleaved_uncleaved.list'
