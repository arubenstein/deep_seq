#!/usr/bin/env python

"""Plot all graph metrics as histograms"""
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

def get_data_from_dict( sequence_dict, label ):
    return [ val[label] for key, val in sequence_dict.items() ]


def main(list_nodes, output_prefix, metric):
    
    sequences = seq_IO.read_sequences(list_nodes, additional_params=True, header=True)

    cleaved_seq = { key : val for key, val in sequences.items() if val["type"] == "CLEAVED" }
    middle_seq = { key : val for key, val in sequences.items() if val["type"] == "MIDDLE" }
    uncleaved_seq = { key : val for key, val in sequences.items() if val["type"] == "UNCLEAVED" }

    if metric == "metrics":
        labels_non_plot = ["label", "fitness", "type", "canonical", "timeset"]
        labels_to_plot = sorted([ key for key in sequences["YNYIN"].keys() if key not in labels_non_plot ] + ["Fraction_Cleaved"])
    else:
	labels_to_plot = [metric]

    n_to_plot = len(labels_to_plot)
    fig, axarr = pconv.create_ax(n_to_plot, 1, shx=False, shy=False)

    nbins = 20    

    for ind, key in enumerate(labels_to_plot):
	if key == "pageranks":
            log = True
	else:
	    log = False
	if key == "Fraction_Cleaved":
            data = [ conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), cleaved_seq.keys()).values(),
		     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), middle_seq.keys()).values(),
                     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), uncleaved_seq.keys()).values()]
	    normed = True
	else:
            data = [ get_data_from_dict(cleaved_seq, key), get_data_from_dict(middle_seq, key), get_data_from_dict(uncleaved_seq, key) ]
	    normed = True
	print key
        hist.draw_actual_plot(axarr[0,ind], data, "", key.capitalize(), log=log, normed=normed, label=["Cleaved", "Middle", "Uncleaved"], nbins=nbins)    
        axarr[0,ind].ticklabel_format(axis='x', style='sci', scilimits=(-2,2))

        #pconv.add_legend(axarr[0,ind], location="middle right")
    pconv.save_fig(fig, output_prefix, "metrics", n_to_plot*5, 5, tight=True, size=12) 

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--list_nodes', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--metric', default="metrics", help='name of metric to plot.  To plot all metrics, input metrics')

    args = parser.parse_args()

    main(args.list_nodes, args.output_prefix, args.metric)
