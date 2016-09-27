#!/bin/bash

python CreateEdges.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved_fitness.csv "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved_fitness.csv "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle_fitness.csv "MIDDLE" --hamming_dist 1 --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq --canonical_file ~/git_repos/deep_seq/analysis_vis/canonical_seqs.txt

python FractionFuncPerMutant.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle.txt "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_cleaved_v_uncleaved --func_labels "CLEAVED" --unfunc_labels "UNCLEAVED" --canonical "DEMEE" 

python FractionFuncPerMutant.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle.txt "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_cleaved_v_uncleaved_middle --func_labels "CLEAVED" --unfunc_labels "UNCLEAVED" "MIDDLE" --canonical "DEMEE"

python FractionFuncPerMutant.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle.txt "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_cleaved_middle_v_uncleaved --func_labels "CLEAVED" "MIDDLE" --unfunc_labels "UNCLEAVED" --canonical "DEMEE"

python FractionFunctional.py --seq_file ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_cleaved_v_uncleaved --canonical "DEMEE"

python FractionNeighborsUncleaved.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_middle.txt "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq_ 

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/101_cleaved.txt "R155K" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/021_cleaved.txt "A156T" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/091_cleaved.txt "D186A" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/011_cleaved.txt "KTA" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/021_cleaved.txt "A156T" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/091_cleaved.txt "D186A" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/011_cleaved.txt "KTA" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/101_cleaved.txt "R155K" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/091_cleaved.txt "D186A" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/011_cleaved.txt "KTA" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/021_cleaved.txt "A156T" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/101_cleaved.txt "R155K" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "WT cleaved" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/011_cleaved.txt "KTA cleaved" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "WT uncleaved" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python VennDiagram.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_cleaved.txt "WT cleaved" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/011_uncleaved.txt "KTA uncleaved" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/WT_nextseq_uncleaved.txt "WT uncleaved" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

python FindSeqs.py --input_dir ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11/ --output_prefix ./ --hamm_dist -1 --canonical_file ~/git_repos/deep_seq/analysis_vis/canonical_seqs.txt 

python EpistasisAllSeqs.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11_norm_counts11/WT_nextseq_cleaved_fitness_ratio.csv "CLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11_norm_counts11/WT_nextseq_uncleaved_fitness_ratio.csv "UNCLEAVED" --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11_norm_counts11/WT_nextseq_middle_fitness_ratio.csv "MIDDLE" --output_prefix ~/git_repos/deep_seq/analysis_vis/results/WT_nextseq

./extract_data_seq_categorize.sh ~/Dropbox/Research/Khare/deep_seq/norm_counts11/summary_WT_nextseq.csv

python convert_seq_features.py --sequence_list ~/git_repos/deep_seq/analysis_vis/seq_lists_norm_counts11_norm_counts11/WT_nextseq_cleaved.txt --conversion_type alpha

python PlotEpistasisDist.py --epistasis results/epistasis/WT_nextseq_epi.csv
