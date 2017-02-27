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
from plot import conv as pconv
from plot import hist 

def main(list_sequence_names, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename) 
        list_sequences.append(sequences)
        extended_list_sequences.extend(sequences[:])
        labels.append(label)

    cleaved_ind = labels.index("CLEAVED")
    middle_ind = labels.index("MIDDLE")
    uncleaved_ind = labels.index("UNCLEAVED")
    frac_uncleaved = {}
    frac_cleaved = {}
    frac_middle = {}
    for seq in list_sequences[cleaved_ind]:
        cleaved_seqs = sum([1 for s in list_sequences[cleaved_ind] if conv.hamdist(seq,s) == 1])
        uncleaved_seqs = sum([1 for s in list_sequences[uncleaved_ind] if conv.hamdist(seq,s) == 1])
        middle_seqs = sum([1 for s in list_sequences[middle_ind] if conv.hamdist(seq,s) == 1])
	if cleaved_seqs > 0 or uncleaved_seqs > 0:
	    total = uncleaved_seqs+middle_seqs+cleaved_seqs
            frac_uncleaved[seq] = float(uncleaved_seqs)/total
	    frac_cleaved[seq] = float(cleaved_seqs)/total
            frac_middle[seq] = float(middle_seqs)/total
    fig, ax = pconv.create_ax(3, 1)

    hist.draw_actual_plot(ax[0,0], frac_cleaved.values(), "Landscape Near Cleaved Sequences", "Fraction of Neighbors Cleaved", log=False, normed=False, nbins=20)
    hist.draw_actual_plot(ax[0,1], frac_middle.values(), "Landscape Near Cleaved Sequences", "Fraction of Neighbors Middle", log=False, normed=False, nbins=20)
    hist.draw_actual_plot(ax[0,2], frac_uncleaved.values(), "Landscape Near Cleaved Sequences", "Fraction of Neighbors Uncleaved", log=False, normed=False, nbins=20)

    pconv.save_fig(fig, output_prefix, "fraction_neighbors", 15, 5, size=10)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)
