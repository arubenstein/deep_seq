#!/bin/bash

regex_files=$1 #quote wildcards in single quotes
outpath=$2
script=$3
server=$4
n_servers=$5
n_cores_per_script=$6


input=($regex_files)

mkdir -p $outpath

if [[ $input =~ "*" || ${#input[@]} -eq 0  ]]
then
	echo "No filenames found"
	exit
fi

#determines begin and end indices based on how many files there are and how many servers there are
n_files=${#input[@]}

n_files_in_group=$(( $n_files / $n_servers + 1 ))
begin_index=$(( $n_files_in_group * ($server-1) ))

echo "Looping"
echo "Filenames are ${input[@]:$begin_index:$n_files_in_group}"

#sets counters
counter=0

n_cores=30

#n_cores_per_script must be a factor of n_cores TODO: output warning if not
if [ ! -z ${n_cores_per_script+x} ];
then
        n_cores=$(( $n_cores / $n_cores_per_script ))
fi

for file in "${input[@]:$begin_index:$n_files_in_group}";
do
        counter=$(( $counter + 1 ))

	echo "Processing $file"

	actual_fn=$(basename $file)
	actual_fn="${actual_fn%.*}"

	echo "Actual filename is $actual_fn"

	$script $file $actual_fn $outpath $server &

        if (( $counter % $n_cores == 0 ));
             then
             wait
        fi

done

wait
