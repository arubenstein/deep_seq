import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse

def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def main(list_sequence_names, hamming_dist, output_prefix):

    list_sequences = []
    extended_list_sequences = []
    labels = []

    for [filename, label] in list_sequence_names:
        with open(filename) as strings:
            sequences = strings.read().splitlines()
            list_sequences.append(sequences)
            extended_list_sequences.extend(sequences[:])
            labels.append(label)
    
    outfile_edges = '%s_edges.csv' % (output_prefix)
    outfile_nodes = '%s_nodes.csv' % (output_prefix)

    edges = ((seq2,seq) for seq,seq2 in itertools.combinations(extended_list_sequences,2) if hamdist(seq2,seq) == hamming_dist )
    
    
    edges_out = open(outfile_edges,"w")
    edges_out.write("Source,Target\n")
    for x in edges:
        edges_out.write("{0},{1}\n".format(x[0],x[1]))

    already_written_nodes = []
   
    nodes_out = open(outfile_nodes,"w")
    nodes_out.write("Id,Label,Type\n")
    for seqs,label in zip(list_sequences,labels):
        nodes_out.write("\n".join("{0},{0},{1}".format(x, label) for x in seqs if x not in already_written_nodes))
        already_written_nodes.extend(seqs)
        nodes_out.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--hamming_dist', default=2, type=int, help='hamming distance to use for calculating edges')

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.hamming_dist, args.output_prefix)
