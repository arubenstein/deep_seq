#!/bin/bash

prelim=$1
prefix=$2

export HOME=~/
export OUTPATH=~/git_repos/deep_seq/designs/results/
export INPATH=~/git_repos/deep_seq/designs/input/
export SCRIPTS=~/git_repos/deep_seq/designs/scripts/
export ROSETTA_BIN=~/Rosetta/main/source/bin/
export ROSETTA_DB=~/Rosetta/main/database/
export XML=~/git_repos/deep_seq/designs/xml/

if [[ $prelim == 1 ]]
then
	#initial mutate from 2fm2 to ly104 sequence
	cd $INPATH'/pdbs/'
	nohup nice $ROSETTA_BIN'/'rosetta_scripts.linuxgccrelease  -jd2:ntrials 1 -nstruct 1 -parser:protocol $XML'/mut_pack.xml' -database $ROSETTA_DB -s ~/git_repos/deep_seq/discrim_sim/input'/pdbs/ly104_CASHL.pdb' -run:preserve_header -resfile $INPATH'/resfile/ly104_R155K.resfile' @/home/arubenstein/git_repos/general_src/enzflags > mut_pack.log
	#mv 2fm2_complex_0001.pdb ly104.pdb
fi

