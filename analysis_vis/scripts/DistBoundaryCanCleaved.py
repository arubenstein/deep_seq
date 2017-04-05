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
from plot import hist 

def main(list_sequence_names, canonical_list, output_prefix ):

    series = []

    canonical_list_seq = seq_IO.read_sequences(canonical_list)

    cleaved_seqs = seq_IO.read_sequences( [ s for s,l in list_sequence_names if l == "CLEAVED" ][0] )

    uncleaved_seqs = seq_IO.read_sequences( [ s for s,l in list_sequence_names if l == "UNCLEAVED" ][0] )

    min_dist = []
    avg_dist = []
    max_dist = []

    for seq in cleaved_seqs:

        distances = [ conv.hamdist(seq, unc) for unc in uncleaved_seqs ]
        min_dist.append(min(distances))
        avg_dist.append(numpy.mean(distances))
        max_dist.append(max(distances))
	if seq in canonical_list_seq:
            print seq
	    print min_dist[-1]
            print avg_dist[-1]
            print max_dist[-1]	
    

    fig, ax = pconv.create_ax(1, 3)


    hist.draw_actual_plot(ax[0,0], min_dist, "Min. Distance from Boundary", "Minimum Distances", log=False, normed=True, label=None, nbins=15, stacked=False)
    hist.draw_actual_plot(ax[1,0], avg_dist, "Avg. Distance from Boundary", "Average Distances", log=False, normed=True, label=None, nbins=15, stacked=False)
    hist.draw_actual_plot(ax[2,0], max_dist, "Max. Distance from Boundary", "Maximum Distances", log=False, normed=True, label=None, nbins=15, stacked=False)


    #ax[0,0].set_xlim(xmin=1,xmax=5)
    #ax[0,0].set_xticks(xrange(1,6))
    pconv.save_fig(fig, output_prefix, "dist_from_bounds", 18, 6, size=15)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument('--canonical_list', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')

    args = parser.parse_args()

    main(args.sequence_list, args.canonical_list, args.output_prefix)

