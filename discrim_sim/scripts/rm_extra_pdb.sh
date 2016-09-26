#!/bin/bash

counter=0
counter_jobs_to_do=0
counter_unequal=0
counter_unequal_other=0

for dir in $(find /scratch/alizarub/git_repos/deep_seq/discrim_sim/results/ -type d -name "???")
do
	if [[ ! -f $dir'/'seqs.list ]]
	then
		continue
	fi 

	cd $dir 
        ls *.pdb > all.list

	if [[ $? != 0 ]] 
	then
		if [ -f $dir'/'seqs.list ]
		then
			counter_jobs_to_do=$((counter_jobs_to_do+1))
		fi
		continue
	fi
        counter=$((counter+1))

	n_pdb=$(wc -l all.list | awk '{print $1}')
	n_list=$(wc -l seqs.list | awk '{print $1}')
	if [[ $n_list -lt $n_pdb ]]
	then
	 	echo $dir
		counter_unequal=$((counter_unequal+1))	
		grep -v -f seqs.list all.list | xargs rm 
	elif [[ $n_list -gt $n_pdb ]]
	then
		echo $dir
		counter_unequal_other=$((counter_unequal_other+1))
	fi

        if [[ $(( $counter % 20 )) == 0 ]]
	then
		wait
	fi

	rm all.list
	rm -f files_to_delete
done

echo $counter_jobs_to_do
echo $counter_unequal
echo $counter_unequal_other
