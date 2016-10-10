#!/bin/bash

path=$1

cd $path

#declare functions
check_file ()
{
	f=$1
	status=1
        if [[ -s $f ]]; then
	    in=( $( < $f ) )
            if [[ $in != "0" ]]; then
	        status=0
		#echo "$1 has already been run"
	    fi
	fi
	return $status
}

for dir in $(ls -l | grep '^d' | awk '{print $9}' )
do
        cd $dir

	#loop through pdb files and run amber on them
	for pdb_name in $(ls *.txt)
	do
		#extract pdb_id
		pn=$(basename $pdb_name '.txt')
		
		#check file before running
		check_file $pn'_dat_complex'
		#if file has not been created then run amber
		if [[ $? -eq 1 ]]
		then
			echo "Amber has not been run yet for $pdb_name"
			if [[  ! -e $pn'.pdb' ]]
			then
				echo "Pdb file does not exist for $pdb_name"
				rm $pn'.txt'
			fi 
		else
		 		
			echo "Amber run already completed for $pdb_name"
		fi

	done
	cd ../
done
