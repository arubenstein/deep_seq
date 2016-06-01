#!/bin/bash

server=$1 #if only running with one server, make the server number be 1
pre_enrich=$2
enrich=$3

export HOME=~/
export OUTPATH=~/git_repos/deep_seq/processing_seqs/results/
export INPATH=~/git_repos/deep_seq/processing_seqs/ancillary_files/
export SCRIPTS=~/git_repos/deep_seq/processing_seqs/scripts/
export ENRICH_BG_LIST=$INPATH'/'enrich_bg_list

easy_install $HOME'/'git_repos/deep_seq/processing_seqs/Enrich-0.2/

if [[ $pre_enrich -eq 1 ]]
then
	#1. split_fasta
	$SCRIPTS'/'loop_pdbs.sh $INPATH'/fasta/*.fasta' $OUTPATH'/'split_fasta $SCRIPTS'/split_fasta.sh' 1 1 1


        #2. seq/processing_seqsorient.pl
	$SCRIPTS'/'loop_pdbs.sh $OUTPATH'/split_fasta/*.fsa' $OUTPATH'/orient/' $SCRIPTS'/orient.sh' 1 1 1

	#3. orient_to_enrich.sh
	$SCRIPTS'/'loop_pdbs.sh $OUTPATH'/orient/*/' $OUTPATH'/pre_enrich/' $SCRIPTS'/orient_to_enrich.sh' 1 1 1
fi

if [[ $enrich -eq 1 ]]
then
	$SCRIPTS'/'loop_pdbs.sh $OUTPATH'/pre_enrich/*_cut.fastq' $OUTPATH'/'enrich'/' $SCRIPTS'/run_enrich.sh' 1 1 1
fi