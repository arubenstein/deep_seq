#!/bin/sh
#SBATCH -J frac_shells 
#SBATCH -o frac_shells.stdout
#SBATCH -e frac_shells.stderr
#SBATCH -p main
#SBATCH -N 1
#SBATCH -t 48:00:00

end_ind=$(($1+23))

for i in $(seq $1 $end_ind)
do
	python2.7 FractionShellsRawUncleaved.py --sequence_list /project1/sdk94-001/git_repos/deep_seq/analysis_vis/svm_results/cleaved_seqs_svm_structseq.list "CLEAVED" --sequence_list /project1/sdk94-001/git_repos/deep_seq/analysis_vis/svm_results/uncleaved_seqs_svm_structseq.list "UNCLEAVED" --output_prefix /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/fraction_shells --index $i &
done

wait
