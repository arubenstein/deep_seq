#!/bin/bash

path=$1
n_files=$2
file_pattern=$3

cd $path

for dir in $(ls -l | grep '^d' | awk '{print $9}' )
do
	cd $dir
	curr_n_files=$(ls $file_pattern | wc -l)
	if [[ $curr_n_files -ne $n_files ]]
	then
		echo $dir
	fi	
	cd ../
done
