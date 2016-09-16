#!/bin/bash

bin=$1
db=$2
inpath=$3
temppath=$4
outpath=$5
sequence=$6
home=$7
scripts=$8
torque=$9

#declare functions
check_file ()
{
	f=$1
	status=1
        if [[ -s $f ]]; then
	    in=( $( < $f ) )
            if [[ $in -ne 0 ]]; then
	        status=0
	    fi
	fi
	return $status
}

#preliminary commands

mkdir -p $temppath'/'$sequence

#copy scorefunction files from db to temppath
cp $db'/scoring/weights/talaris2014.wts' $temppath'/'$sequence
cp $db'/scoring/weights/talaris2014_cst.wts' $temppath'/'$sequence

if [[ $torque -eq 1 ]]
then
	#in case restarting from previous job, copy any old files back
	cp -r $outpath'/'$sequence'/'* $temppath'/'$sequence
fi

cd $temppath'/'$sequence

#Rosetta part
#first kick off command to copy all files at 23:30 hours past this time. this will run in the background.
$scripts'/'rsync_files.sh $temppath'/'$sequence'/' $outpath'/'$sequence'/' &

#run command should place output files (pdb, txt, and silent file) in the temppath folder
$bin/discrim_sim.static.linuxgccrelease -database $db -s $inpath/pdbs/ly104_CASHL.pdb -out::path::pdb $temppath -enzdes::cstfile $inpath/pdbs/ly104cstfile.txt -run:preserve_header "@"$home"/"git_repos/general_src/enzflags -out::prefix $sequence -resfile $inpath/resfile/rfpackpept.txt

cp -r $temppath'/'$sequence'/'* $outpath'/'$sequence'/'

#loop through pdb files and run amber on them
for pdb_name in $(ls *.pdb)
do
	#extract pdb_id
	pn=$(basename $pdb_name '.pdb')
	
	#check file before running
	check_file $pn'_dat_complex'
	#if file has not been created then run amber
	if [[ $? -eq 1 ]]
	then
		$scripts'/amber_run_file.sh' $pn $temppath'/'$sequence $scripts $torque
	else
		echo "Amber run already completed for $pdb_name"
	fi

	#check file after running amber
	check_file $pn'_dat_complex'
	#if file has been created then rm pdb files
        if [[ $? -eq 0 ]]; then
		rm $pdb_name
		#in case restarting from previous job 
		rm -f $outpath'/'$sequence'/'$pn'.pdb'
	else
		echo "Warning - amber run did not complete and pdb file $pdb_name has not yet been deleted"
	fi
done

 move all data back
cp -r $temppath'/'$sequence'/'* $outpath'/'$sequence'/'
