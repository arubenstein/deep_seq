#!/usr/bin/env python

"""Create edges and nodes from a list of sequences that are a given hamming distance apart"""
import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from general_seq import conv
from general_seq import seq_IO

def main(list_sequence_names, hamming_dist, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float})
        list_sequences.append(sequences)
        extended_list_sequences.extend(sequences[:])
        labels.append(label)

    outfile_edges = '%s_edges.csv' % (output_prefix)
    outfile_nodes = '%s_nodes.csv' % (output_prefix)

    edges = ((seq2,seq) for seq,seq2 in itertools.combinations(extended_list_sequences,2) if conv.hamdist(seq2[0],seq[0]) == hamming_dist )

    canonical_seq = "DEMEE"    
    
    edges_out = open(outfile_edges,"w")
    edges_out.write("Source,Target,Weight\n")
    for ([seq1,fit1],[seq2,fit2]) in edges:
        dist_seq1 = conv.hamdist(canonical_seq, seq1)
        dist_seq2 = conv.hamdist(canonical_seq, seq2)
        fit_lower = fit1 if dist_seq1 < dist_seq2 else fit2
        fit_upper = fit2 if dist_seq1 < dist_seq2 else fit1
        fit_upper = fit_upper if fit_upper > 0 else 0.001
        
        edges_out.write("{0},{1},{2}\n".format(seq1,seq2,fit_lower/float(fit_upper))) #does this have the correct directionality?

    already_written_nodes = []
   
    nodes_out = open(outfile_nodes,"w")
    nodes_out.write("Id,Label,Type,Fitness\n")
    for seqs,label in zip(list_sequences,labels):
        nodes_out.write("\n".join("{0},{0},{1},{2}".format(x, label, fitness) for (x,fitness) in seqs if x not in already_written_nodes))
        already_written_nodes.extend([ s[0] for s in seqs])
        nodes_out.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--hamming_dist', default=2, type=int, help='hamming distance to use for calculating edges')

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.hamming_dist, args.output_prefix)
