#!/bin/bash

counter=0
counter_jobs_to_do=0
counter_unequal=0

for dir in $(find ~/git_repos/deep_seq/discrim_sim/results/ -type d -name "???")
do
	if [[ ! -f $dir'/'$(basename $dir) ]]
	then
		continue
	fi 

	cd $dir 
	echo $dir
        ls *.pdb > all.list

	if [[ $? != 0 ]] && [ -f $dir'/'seqs.list ]
	then
		echo "Still have to run"
		counter_jobs_to_do=$((counter_jobs_to_do+1))
		continue
	fi
        counter=$((counter+1))

	n_pdb=$(wc -l all.list | awk '{print $1}')
	ls all.list
	n_list=$(wc -l seqs.list | awk '{print $1}')
	if [[ $n_list -lt $n_pdb ]]
	then
		echo $n_list
		echo $n_pdb
	 	counter_unequal=$((counter_unequal+1))	
		grep -v -f seqs.list all.list | xargs rm 
	fi

        if [[ $(( $counter % 20 )) == 0 ]]
	then
		echo "waiting"
		wait
	fi

	rm all.list
	rm -f files_to_delete
done

echo $counter_jobs_to_do
echo $counter_unequal
