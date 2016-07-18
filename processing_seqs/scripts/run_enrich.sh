#!/bin/bash

file=$1
actual_fn=$2
outpath=$3
server=$4
threshold=$5

export PATH="${PATH}:/home/arubenstein/dist-packages"
export PYTHONPATH="${PYTHONPATH}:/home/arubenstein/dist-packages"

background=( $( < $ENRICH_BG_LIST ) )

for bg_full in "${background[@]}"
do

     IFS=',' read -ra sep <<< "$bg_full"
     bg=${sep[0]}
     supposed_sel=${sep[1]}

     bg_file=$OUTPATH'/'pre_enrich'/'$bg'_cut.fastq'
     length=$(( ${#actual_fn} - 4 ))
     sel_name=${actual_fn:0:$length}

     if [[ $supposed_sel != $sel_name ]]
     then
	continue
     fi

     enrich_dir=$outpath'/'$bg'_'$sel_name  
     template_enrich=$HOME'/git_repos/deep_seq/processing_seqs/enrich_template/input/enrich_default_config'
     enrich_def_config=$enrich_dir'/input/enrich_default_config'
         
     enrich_new_config=$enrich_dir'/input/test'   

     #check that hasn't been run already
     ratios=( $enrich_dir'/'data/output/ratios* )

     if [[ ${#ratios[@]} -eq 6 ]]
     then
         echo $bg'_'$sel_name" has already been run"
         continue
     fi

     mkdir -p $enrich_dir'/'input/
     mkdir -p $enrich_dir'/'data/raw/
     mkdir -p $enrich_dir'/'data/output/
     mkdir -p $enrich_dir'/'data/tmp/
     mkdir -p $enrich_dir'/'log/
     mkdir -p $enrich_dir'/'plots/

     cp -r $template_enrich $enrich_dir'/input/'

     cp $enrich_def_config $enrich_new_config 
     
     ln -s $bg_file $enrich_dir'/data/raw/'$bg.fastq
     ln -s $file $enrich_dir'/data/raw/'$sel_name.fastq

     #change name of sel and unsel files
     sed -i 's/dummy1/'$bg'/g' $enrich_new_config
     sed -i 's/dummy2/'$sel_name'/g' $enrich_new_config

     #change name of path in config file
     sed -i 's:PATH_REP:'$outpath'/'$bg'_'$sel_name'/:g' $enrich_new_config
     sed -i 's:COUNTS_THRESHOLD:'$threshold':g' $enrich_new_config
     sed -i 's/dummy_run_name/'$bg'_'$sel_name'/g' $enrich_new_config

     enrich --mode read_fuse --config_file $enrich_new_config
     enrich --mode read_align --config_file $enrich_new_config
     enrich --mode map_counts --config_file $enrich_new_config
     enrich --mode map_ratios --config_file $enrich_new_config
     #enrich --mode map_unlink --config_file $enrich_new_config
     rm $enrich_dir'/data/tmp/'*
done

