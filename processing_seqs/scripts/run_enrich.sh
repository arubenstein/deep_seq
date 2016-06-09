#!/bin/bash

file=$1
actual_fn=$2
outpath=$3
server=$4

export PATH="${PATH}:/home/arubenstein/dist-packages"
export PYTHONPATH="${PYTHONPATH}:/home/arubenstein/dist-packages"

background=( $( < $ENRICH_BG_LIST ) )

echo ${background[@]}

for bg in "${background[@]}"
do
     bg_file=$OUTPATH'/'pre_enrich'/'$bg'_cut.fastq'
     length=$(( ${#actual_fn} - 4 ))
     sel_name=${actual_fn:0:$length}

     if [[ $bg == $sel_name ]]
     then
	continue
     fi

     enrich_dir=$outpath'/'$bg'_'$sel_name  
     enrich_def_config=$enrich_dir'/input/enrich_default_config'
     enrich_new_config=$enrich_dir'/input/test'   

     mkdir -p $enrich_dir'/'input/
     mkdir -p $enrich_dir'/'data/raw/
     mkdir -p $enrich_dir'/'data/output/
     mkdir -p $enrich_dir'/'data/tmp/
     mkdir -p $enrich_dir'/'log/
     mkdir -p $enrich_dir'/'plots/

     cp -r $HOME'/git_repos/deep_seq/processing_seqs/enrich_template/input/enrich_default_config' $enrich_dir'/input/'

     cp $enrich_def_config $enrich_new_config 
     
     cp $bg_file $enrich_dir'/data/raw/'$bg.fastq
     cp $file $enrich_dir'/data/raw/'$sel_name.fastq

     #change name of sel and unsel files
     sed -i 's/dummy1/'$bg'/g' $enrich_new_config
     sed -i 's/dummy2/'$sel_name'/g' $enrich_new_config

     #change name of path in config file
     sed -i 's/enrich_template/'$bg'_'$sel_name'/g' $enrich_new_config

     sed -i 's/dummy_run_name/'$bg'_'$sel_name'/g' $enrich_new_config

     enrich --mode read_fuse --config_file $enrich_new_config
     enrich --mode read_align --config_file $enrich_new_config
     enrich --mode map_counts --config_file $enrich_new_config
     enrich --mode map_ratios --config_file $enrich_new_config
     enrich --mode map_unlink --config_file $enrich_new_config

done

