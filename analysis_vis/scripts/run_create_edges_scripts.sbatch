#!/bin/sh
#SBATCH -J create_edges 
#SBATCH -o create_edges.stdout
#SBATCH -e create_edges.stderr
#SBATCH -p main
#SBATCH -n 1
#SBATCH -t 48:00:00
#SBATCH -mem 10240

#python2.7 ShortestPaths.py --json_file ../results/graph_inputs/SVM_fullNXnodes_edges.json --output_prefix ../results/graph_outputs/SVM_full --source 'DEMEE' --target "AEMEE"

python2.7 CreateEdgesNX.py --sequence_list /project1/sdk94-001//git_repos/deep_seq/analysis_vis/svm_results/cleaved_seqs_svm_structseq.txt "CLEAVED" --sequence_list /project1/sdk94-001/git_repos/deep_seq/analysis_vis/svm_results/uncleaved_seqs_svm_structseq.txt "UNCLEAVED" --hamming_dist 1 --output_prefix /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/graph_inputs/SVM_fullNX --canonical_file ""
