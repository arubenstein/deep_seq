#!/bin/bash

silent_file=$1
list_seqs=$2

#check that file exists
#if [ ! -f $silent_file ]
#then
#	echo "$silent_file not found"
#	exit
#fi

#check that has not already been extracted

done=0

#if [[ $list_seqs != "" ]]
#then
#	cd $(dirname $silent_file)
#	n_pdb=$(ls *.pdb | wc -l)
#        n_list=$(wc -l $list_seqs | awk '{print $1}')
#        if [[ $n_list == $n_pdb ]]
#	then
#		done=1
#	fi
#fi


	sed -i 's/SER_connectOG/SER:MP-OG-connect/g' $silent_file
	sed -i 's/CYS_connectC/CYS:MP-C-connect/g' $silent_file
	sed -i 's/home/scratch/g' $silent_file
        sed -i 's/arubenstein/alizarub/g' $silent_file
	nohup nice ~/Rosetta/main/source/bin/extract_pdbs.static.linuxgccrelease -database ~/Rosetta/main/database/ -in::file::silent $silent_file > $silent_file'.log'

if [[ $list_seqs == "" ]]
then
	list_seqs=$(dirname $silent_file)'/'seqs.list
	if [ ! -f $list_seqs ]
	then
		exit
	fi
fi

dir=$(dirname $silent_file)

cd $dir

ls *.pdb > list

grep -v -f $list_seqs list | xargs rm

rm list

chmod 777 *.pdb
