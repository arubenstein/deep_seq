#!/bin/sh
#SBATCH -J nx_script
#SBATCH -o nx_script.stdout
#SBATCH -e nx_script.stderr
#SBATCH -p main
#SBATCH -n 1
#SBATCH -t 24:00:00
#SBATCH --mem=10240

#python2.7 /project1/sdk94-001/git_repos/deep_seq/analysis_vis/scripts/NXRawMetrics.py --json_file /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/graph_inputs/SVM_full_cleaved_NXnodes_edges.json --output_prefix /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/graph_outputs/SVM_full_cleaved

python2.7 FracShortestPaths.py --json_file /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/graph_inputs/SVM_fullNXnodes_edges.json --output_prefix /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/graph_outputs/frac_shortest_paths --novel_seqs_file /project1/sdk94-001/git_repos/deep_seq/analysis_vis/results/svm_analysis/more_2_over80.txt --canonical_file ../input/canonical_seqs.txt
