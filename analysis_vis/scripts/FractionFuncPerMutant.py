#!/usr/bin/env python

"""Plots fraction functional variants # of mutations away from consensus seq."""

import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from general_seq import conv
from general_seq import seq_IO
from plot import conv as pconv
from plot import scatterplot 

def main(list_sequence_names, canonical_list, output_prefix, func_labels, unfunc_labels):

    series = []

    canonical_list_seq = seq_IO.read_sequences(canonical_list)

    for canonical in canonical_list_seq:
	
        dict_sequences = {}

        for [filename, label] in list_sequence_names:
            sequences = seq_IO.read_sequences(filename) 
            distances = [ conv.hamdist(seq, canonical) for seq in sequences ]
        
            dict_sequences[label] =  { i : sum([d for d in distances if d == i]) for i in xrange(1,6) } 

        x = []
        y = []
        for i in xrange(1,6):
            func=0.0
            unfunc=0.0
            for label, dict_sums in dict_sequences.items():
                if label in func_labels:
                    func = func + dict_sums[i]
                elif label in unfunc_labels:
                    unfunc = unfunc + dict_sums[i]
            if unfunc != 0:
		x.append(i)
                y.append( func/(func+unfunc) )
        print x
	print y
        series.append([x, y, canonical])
    fig, ax = pconv.create_ax(1, 1)

    scatterplot.plot_series( ax[0,0], series, title="", x_axis="# of Mutations", y_axis="Fraction of Variants that are Functional", alpha=1.0, connect_dots=True, size=30, edgecolors='k')
    ax[0,0].set_xlim(xmin=1,xmax=5)
    ax[0,0].set_xticks(xrange(1,6))
    pconv.save_fig(fig, output_prefix, canonical + "_fraction_func_mutant", 6, 6, size=15)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument('--canonical_list', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')
    parser.add_argument('--func_labels', nargs='+', help='Which labels are for functional variants?')
    parser.add_argument('--unfunc_labels', nargs='+', help='Which labels are for functional variants?')

    args = parser.parse_args()

    main(args.sequence_list, args.canonical_list, args.output_prefix, args.func_labels, args.unfunc_labels)

