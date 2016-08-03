#!/bin/bash

python CreateEdges.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_cleaved_fitness.csv "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_uncleaved_fitness.csv "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_middle_fitness.csv "MIDDLE" --hamming_dist 1 --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python FractionFuncPerMutant.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_cleaved.txt "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_uncleaved.txt "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists/WT_nextseq_middle.txt "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_cleaved_v_uncleaved --func_labels "CLEAVED" --unfunc_labels "UNCLEAVED" --canonical "DEMEE" 

