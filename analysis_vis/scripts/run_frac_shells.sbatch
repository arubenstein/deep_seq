#!/bin/sh
#SBATCH -J frac_shells 
#SBATCH -o frac_shells.stdout
#SBATCH -e frac_shells.stderr
#SBATCH -p main
#SBATCH -n 1
#SBATCH -t 48:00:00

python2.7 FractionShellsRaw.py --sequence_list /project1/sdk94-001/git_repos/deep_seq/analysis_vis/svm_results/cleaved_seqs_svm_structseq.list "CLEAVED" --sequence_list /project1/sdk94-001/git_repos/deep_seq/analysis_vis/svm_results/uncleaved_seqs_svm_structseq.list "UNCLEAVED" --output_prefix /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/fraction_shells --index $1
