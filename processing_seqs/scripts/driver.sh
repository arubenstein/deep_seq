#!/bin/bash

server=$1 #if only running with one server, make the server number be 1
pre_enrich=$2
enrich=$3
nextseq=$4
threshold=$5

export HOME=~/
export OUTPATH=~/git_repos/deep_seq/processing_seqs/results/
export INPATH=~/git_repos/deep_seq/processing_seqs/ancillary_files/
export SCRIPTS=~/git_repos/deep_seq/processing_seqs/scripts/
export ENRICH_BG_LIST=$INPATH'/'enrich_bg_list
export ENRICH_CL_UNCL_LIST=$INPATH'/'enrich_cl_uncl_list

mkdir -p $HOME'/dist-packages/'
easy_install -d $HOME'/'dist-packages/ $HOME'/'git_repos/deep_seq/processing_seqs/Enrich-0.2/

if [[ $pre_enrich -eq 1 ]]
then
	if [[ $nextseq -eq 0 ]]
	then
		#1. split_fasta
		$SCRIPTS'/'loop_pdbs.sh $INPATH'/fasta/miseq/*.fasta' $OUTPATH'/'split_fasta $SCRIPTS'/split_fasta.sh' 1 1 1

		#2. seq_orient.pl
		$SCRIPTS'/'loop_pdbs.sh $OUTPATH'/split_fasta/*.fsa' $OUTPATH'/orient/' $SCRIPTS'/orient.sh' 1 1 1
		
		#3. orient_to_enrich.sh
		$SCRIPTS'/'loop_pdbs.sh $OUTPATH'/orient/*/' $OUTPATH'/pre_enrich/' $SCRIPTS'/orient_to_enrich.sh' 1 1 1 
	else
		$SCRIPTS'/'loop_pdbs.sh $INPATH'/fasta/nextseq/*.fasta' $OUTPATH'/pre_enrich/' $SCRIPTS'/prep_enrich.sh' 1 1 1
	fi
fi

if [[ $enrich -eq 1 ]]
then
    max_seq=$(wc -l "$OUTPATH"/pre_enrich/*_cut.fastq | awk '{print $1}' | head -n -1 | sort -n | tail -n 1)
    export COUNTS_NORM=$(( max_seq / 4 ))
    print $COUNTS_NORM
    if [[ $threshold == "all" ]]
    then
        for i in `seq 1 30`
	do
            $SCRIPTS'/'loop_pdbs.sh $OUTPATH'/pre_enrich/MP*Tr20*_cut.fastq' $OUTPATH'/enrich/'$i'/' $SCRIPTS'/run_enrich.sh' 1 1 1 $i
            $SCRIPTS'/'postprocess.sh $OUTPATH'/enrich/'$i'/' &	
        done
    else
        $SCRIPTS'/'loop_pdbs.sh $OUTPATH'/pre_enrich/MP*Q20*_cut.fastq' $OUTPATH'/enrich/'$threshold'/' $SCRIPTS'/run_enrich.sh' 1 1 1 $threshold
        #$SCRIPTS'/'postprocess.sh $OUTPATH'/enrich/'$threshold'/'  &
    fi
fi
