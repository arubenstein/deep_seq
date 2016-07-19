#!/bin/bash

export HOME=~/
export OUTPATH=~/git_repos/deep_seq/discrim_sim/results/
export INPATH=~/git_repos/deep_seq/discrim_sim/input/
export SCRIPTS=~/git_repos/deep_seq/discrim_sim/scripts/
export ROSETTA_BIN=~/Rosetta/main/source/bin/
export ROSETTA_DB=~/Rosetta/main/database/
export XML=~/git_repos/deep_seq/discrim_sim/xml/

if [[ $prelim == 1 ]]
then
	#initial mutate from 2fm2 to ly104 sequence
	cd $INPATH'/pdbs/'
	nohup nice $ROSETTA_BIN'/'rosetta_scripts.linuxgccrelease  -jd2:ntrials 1 -nstruct 1 -parser:protocol $XML'/mut_pack.xml' -database $ROSETTA_DB -s $INPATH'/pdbs/2fm2_complex.pdb' -run:preserve_header -resfile $INPATH'/resfile/2fm2_ly104.resfile' @/home/arubenstein/git_repos/general_src/enzflags > mut_pack.log
	mv 2fm2_complex_0001.pdb ly104.pdb
fi

nohup nice $ROSETTA_BIN'/'discrim_sim.linuxgccrelease -database $ROSETTA_DB -s ~/mean_field/relax_decoys/ly104_no_optH/Job_1/Job_1ly104_0001.pdb -enzdes::cstfile /home/arubenstein/git_repos/deep_seq/discrim_sim/input/pdbs/ly104cstfile.txt -run:preserve_header @/home/arubenstein/git_repos/general_src/enzflags > sim.log
