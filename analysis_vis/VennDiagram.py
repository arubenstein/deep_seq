#!/usr/bin/env python

"""Plots fraction functional variants # of mutations away from consensus seq."""

import argparse
from general_seq import seq_IO
from general_seq import conv
from plot import conv as pconv
from matplotlib_venn import venn3

def main(list_sequence_names, output_prefix):

    sequence_list = []
    labels = []

    for [filename, label] in list_sequence_names:
        sequence_list.append(set(seq_IO.read_sequences(filename)))
        labels.append(label) 

    fig, ax = pconv.create_ax(1, 1)

    venn3(sequence_list, set_labels = labels, ax=ax[0,0]) 
    
    pconv.save_fig(fig, output_prefix, '_'.join(labels)+"_venn", 10, 10, size=12)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument('--output_prefix', help='Prefix for output plot files')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)

