#!/bin/bash

for i in {1..9}
do
	start_ind=$(((i-1)*24+1))
	sbatch ./run_frac_shells_uncleaved.sbatch $start_ind
done
