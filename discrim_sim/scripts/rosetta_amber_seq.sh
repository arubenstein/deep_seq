#!/bin/bash

bin=$1
db=$2
inpath=$3
temppath=$4
outpath=$5
prefix=$6
sequence=$7
home=$8
scripts=$9
queue_type=${10}

#declare functions
check_file ()
{
	f=$1
	status=1
        if [[ -s $f ]]; then
	    in=( $( < $f ) )
            if [[ $in != "0" ]]; then
	        status=0
		echo "$1 has already been run"
	    fi
	fi
	return $status
}

#preliminary commands

mkdir -p $temppath'/'$prefix

#copy scorefunction files from db to temppath
cp $db'/scoring/weights/talaris2014.wts' $temppath'/'$prefix
cp $db'/scoring/weights/talaris2014_cst.wts' $temppath'/'$prefix

#in case restarting from previous job, copy any old files back
rsync -av --exclude="*.log" --exclude="*.out" --delete-after $outpath'/'$prefix'/' $temppath'/'$prefix

cd $temppath'/'$prefix

#Rosetta part

if [[ $queue_type == "torque" ]]
then
	#first kick off command to copy all files at 23:30 hours past this time. this will run in the background.
	$scripts'/'rsync_files.sh $temppath'/'$prefix'/' $outpath'/'$prefix'/' &
fi

#run command should place output files (pdb, txt, and silent file) in the temppath folder
$bin/discrim_sim.static.linuxgccrelease -database $db -s $inpath/pdbs/ly104_CASHL.pdb -out::path::pdb $temppath -enzdes::cstfile $inpath/pdbs/ly104cstfile.txt -run:preserve_header "@"$home"/"git_repos/general_src/enzflags -out::prefix $sequence -resfile $inpath/resfile/rfpackpept.txt

rsync -av --exclude="*.log" --exclude="*.out"  $temppath'/'$prefix'/'* $outpath'/'$prefix'/'

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
		$scripts'/amber_run_file.sh' $pn $temppath'/'$prefix $scripts $queue_type
	else
		echo "Amber run already completed for $pdb_name"
	fi

	#check file after running amber
	check_file $pn'_dat_complex'
	#if file has been created then rm pdb files
        if [[ $? -eq 0 ]]; then
		rm $pdb_name
		#in case restarting from previous job 
	else
		echo "Warning - amber run did not complete and pdb file $pdb_name has not yet been deleted"
	fi
done

#move all data back
rsync -av --exclude="*.log" --exclude="*.out"  $temppath'/'$prefix '/'* $outpath'/'$prefix'/'

for pdb_name in $(ls $outpath'/'$prefix'/'*.pdb)
do
        pn=$(basename $pdb_name '.pdb')

        #check file after running amber
        check_file $pn'_dat_complex'
        #if file has been created then rm pdb files
        if [[ $? -eq 0 ]]; then
                rm -f $pdb_name
                #in case restarting from previous job 
                rm -f $outpath'/'$prefix'/'$pn'.pdb'
        else
                echo "Warning - amber run did not complete and pdb file $pdb_name has not yet been deleted"
        fi
done
