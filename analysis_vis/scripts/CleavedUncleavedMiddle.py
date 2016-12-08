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
from plot import bar 

def main(list_sequence_names, output_prefix):

    lines = []

    temp_dict = { "CLEAVED" : {}, "UNCLEAVED" : {}, "MIDDLE" : {} }

    for [filename, label, sample] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename)
        temp_dict[label][sample] = len(sequences)

    lines.append(([ val for k, val in sorted(temp_dict["CLEAVED"].items()) ], "CLEAVED") )
    lines.append(([ val for k, val in sorted(temp_dict["MIDDLE"].items()) ], "MIDDLE") )
    lines.append(([ val for k, val in sorted(temp_dict["UNCLEAVED"].items()) ], "UNCLEAVED") )

    fig, ax = pconv.create_ax(1, 1)

    bar.plot_series( ax[0,0], lines, title="", x_axis="Variant Name", y_axis="Number of Substrate Sequences Sampled", tick_label=sorted(temp_dict["CLEAVED"].keys())) 
    pconv.save_fig(fig, output_prefix, "cleaved_uncleaved_middle", 6, 6, tight=True, size=10)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--sequence_list', '-d', nargs=3, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument('--output_prefix', help='Prefix for output plot files')
    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)

