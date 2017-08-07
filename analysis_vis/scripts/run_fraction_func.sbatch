#!/bin/bash

#SBATCH --partition=main         # Partition (job queue)
#SBATCH --job-name=fracfunc	 # Assign an 8-character name to your job, no spaces
#SBATCH --nodes=1                # Number of compute nodes
#SBATCH --ntasks=1               # Processes (usually = cores) on each node
#SBATCH --cpus-per-task=1        # Threads per process (or per core)
#SBATCH --mem=256000               # Total real memory required (MB) for each node
#SBATCH --time=20:00:00          # Total run time limit (HH:MM:SS)
#SBATCH --output=slurm.%j.out # Combined STDOUT and STDERR output file
#SBATCH --export=ALL             # Export you current environment settings to the job environment

python2.7 EpistasisAllSeqs.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved_fitness_ratio.csv "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved_fitness_ratio.csv "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle_fitness_ratio.csv "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_random

#python FractionFunctionalAllRaw.py --seq_file ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt --canonical_file ~/git_repos/deep_seq/analysis_vis/input/canonical_seqs.txt  --output_prefix ./all_2
