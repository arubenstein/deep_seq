#!/bin/bash

bin=$1
db=$2
inpath=$3
outpath=$4
sequence=$5


$bin/discrim_sim.static.linuxgccrelease -database $db -s $inpath/pdbs/ly104_CASHL.pdb -out::path::pdb $outpath -enzdes::cstfile $inpath/pdbs/ly104cstfile.txt -run:preserve_header @/home/arubenstein/git_repos/general_src/enzflags -out::prefix $sequence -resfile $inpath/resfile/rfpackpept.txt

cd $outpath'/'$sequence

for pdb_name in $(ls *.pdb)
do
	pn=$(basename $pdb_name '.pdb')
	$inpath'/scripts/amber_run_file.sh' $pn $outpath'/'$sequence
	if [[ -f $pn'_dat_complex' ]]
	then
		rm $pdb_name 
	else
		echo "Warning - amber run did not complete and pdb file $pdb_name has not yet been deleted"
	fi
done
