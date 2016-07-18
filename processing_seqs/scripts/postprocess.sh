#!/bin/bash

outpath=$1

export PATH="${PATH}:/home/arubenstein/dist-packages"
export PYTHONPATH="${PYTHONPATH}:/home/arubenstein/dist-packages"

list_names=( $( < $ENRICH_CL_UNCL_LIST ) )

cd $outpath

for names in "${list_names[@]}"
do

     IFS=',' read -ra sep <<< "$names"
     cl=${sep[0]}
     mid=${sep[1]}
     uncl=${sep[2]}

     cl_full_path=$(ls $outpath'/'$cl'/data/output/ratios'_*_PRO_qc )
     mid_full_path=$(ls $outpath'/'$mid'/data/output/ratios'_*_PRO_qc )
     uncl_full_path=$(ls $outpath'/'$uncl'/data/output/ratios'_*_PRO_qc )

     awk ' NR != 1 && $2 !~ /\*/ && $8 > 0 {print $2}'  $cl_full_path | sort > $cl'_positive.txt'
     awk ' NR != 1 && $2 !~ /\*/ && $8 > 0 {print $2}'  $mid_full_path | sort > $mid'_positive.txt'
     awk ' NR != 1 && $2 !~ /\*/ && $8 > 0 {print $2}'  $uncl_full_path | sort > $uncl'_positive.txt'

     comm -1 -2 $cl'_positive.txt' $mid'_positive.txt' > $cl'_'$mid'_overlap.txt'
     comm -1 -2 $cl'_positive.txt' $uncl'_positive.txt' > $cl'_'$uncl'_overlap.txt'
     comm -1 -2 $uncl'_positive.txt' $mid'_positive.txt' > $uncl'_'$mid'_overlap.txt'

     grep -v -f $cl'_'$mid'_overlap.txt' $cl'_positive.txt' > temp.txt
     grep -v -f $cl'_'$uncl'_overlap.txt' temp.txt > $cl'_only.txt'

     grep -v -f $uncl'_'$mid'_overlap.txt' $uncl'_positive.txt' > temp.txt
     grep -v -f $cl'_'$uncl'_overlap.txt' temp.txt > $uncl'_only.txt' 

     rm temp.txt
     echo "looping through $names"
done

echo "concatenating files"
cat MP02Tr20_Fr3_MP07Tr20_Fr3_only.txt MP02Tr20_Fr3_MP72Tr20_Fr3_only.txt > MP02Tr20_Fr3_MP0772Tr20_Fr3_only.txt
cat MP02Tr20_Fr3_MP08Tr20_Fr3_only.txt MP02Tr20_Fr3_MP82Tr20_Fr3_only.txt > MP02Tr20_Fr3_MP0882Tr20_Fr3_only.txt
cat MP02Tr20_Fr3_MP09Tr20_Fr3_only.txt MP02Tr20_Fr3_MP92Tr20_Fr3_only.txt > MP02Tr20_Fr3_MP0992Tr20_Fr3_only.txt
echo "done concatenating files"

