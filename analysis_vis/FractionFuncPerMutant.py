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
from plot import line 

def main(list_sequence_names, canonical, output_prefix, func_labels, unfunc_labels):

    dict_sequences = {}

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename) 
        distances = [ conv.hamdist(seq, canonical) for seq in sequences ]
        
        dict_sequences[label] =  { i : sum([d for d in distances if d == i]) for i in xrange(1,6) } 

    x = [0]
    y = [1]

    for i in xrange(1,6):
        x.append(i)
        func=0.0
        unfunc=0.0
        for label, dict_sums in dict_sequences.items():
            if label in func_labels:
                func = func + dict_sums[i]
            elif label in unfunc_labels:
                unfunc = unfunc + dict_sums[i]
        y.append( func/(func+unfunc) )
    print x
    print y
    fig, ax = pconv.create_ax(1, 1)

    line.draw_actual_plot( x, y, "", ax[0,0], title="Fraction of Mutants Which are Functional", x_axis="# of Mutations", y_axis="Fraction of Variants that are Functional")
    ax[0,0].set_xlim(xmin=1)
    pconv.save_fig(fig, output_prefix, canonical + "_fraction_func_mutant", 6, 6, size=15)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument('--canonical', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')
    parser.add_argument('--func_labels', nargs='+', help='Which labels are for functional variants?')
    parser.add_argument('--unfunc_labels', nargs='+', help='Which labels are for functional variants?')

    args = parser.parse_args()

    main(args.sequence_list, args.canonical, args.output_prefix, args.func_labels, args.unfunc_labels)

