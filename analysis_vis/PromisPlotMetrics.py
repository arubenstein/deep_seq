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
from collections import Counter

def get_data_from_dict( sequence_dict, label ):
    list_metrics = [ val[label] for key, val in sequence_dict.items() ]
    return list_metrics

def average_metrics( dict_metrics, metric_labels ):
    averaged_metrics = { s : {} for s in dict_metrics.keys() }
    
    for seq, list_metrics in dict_metrics.items():
        for label in metric_labels:
	    l = [ val[label] for val in list_metrics ]
            averaged_metrics[seq][label] = float(sum(l))/len(l)
            
    return averaged_metrics
def list_metrics( cleaved_seq_dict, sequences, labels ):
    dict_metrics = {}
    for seq in sequences:
	list_metrics = [ d.get(seq) for d in cleaved_seq_dict.values() if d.get(seq) is not None ] 
        dict_metrics[seq] = list_metrics

    return average_metrics(dict_metrics, labels) 

def main(list_nodes, output_prefix, metric):

    cleaved_seq = {}
    uncleaved_seq = {}
    middle_seq = {}    

    for nodes, label in list_nodes:
        sequences = seq_IO.read_sequences(nodes, additional_params=True, header=True)

        cleaved_seq[label] = { key : val for key, val in sequences.items() if val["type"] == "CLEAVED" }
        middle_seq[label] = { key : val for key, val in sequences.items() if val["type"] == "MIDDLE" }
        uncleaved_seq[label] = { key : val for key, val in sequences.items() if val["type"] == "UNCLEAVED" }

    if metric == "metrics":
        labels_non_plot = ["label", "fitness", "type", "canonical"]
	orig_labels_to_plot = sorted([ key for key in sequences["DEMEE"].keys() if key not in labels_non_plot ])
        labels_to_plot = sorted(orig_labels_to_plot + ["Fraction_Cleaved"])
    else:
	orig_labels_to_plot = [metric]
	labels_to_plot = [metric]

    n_to_plot = len(labels_to_plot)
    fig, axarr = pconv.create_ax(n_to_plot, 1, shx=False, shy=False)

    nbins = 20    

    list_seqs = [ k for d in cleaved_seq.values() for k in d.keys() ]

    count_seqs = Counter(list_seqs)

    seqs_5 = list_metrics( cleaved_seq, [ s for s in list_seqs if count_seqs[s] == 5 ], orig_labels_to_plot)
    seqs_4 = list_metrics( cleaved_seq, [ s for s in list_seqs if count_seqs[s] == 4 ], orig_labels_to_plot)
    seqs_3 = list_metrics( cleaved_seq, [ s for s in list_seqs if count_seqs[s] == 3 ], orig_labels_to_plot)
    seqs_2 = list_metrics( cleaved_seq, [ s for s in list_seqs if count_seqs[s] == 2 ], orig_labels_to_plot)
    seqs_1 = list_metrics( cleaved_seq, [ s for s in list_seqs if count_seqs[s] == 1 ], orig_labels_to_plot)

    for ind, key in enumerate(labels_to_plot):
	if key == "pageranks":
            log = True
	else:
	    log = False
	if key == "Fraction_Cleaved":
            data = [ conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), seqs_5),
                     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), seqs_4),
                     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), seqs_3),
                     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), seqs_2),
                     conv.fraction_neighbors_cleaved(cleaved_seq.keys(), uncleaved_seq.keys(), middle_seq.keys(), seqs_1)]
	    normed=False
        else:
            data = [ get_data_from_dict(seqs_5, key), get_data_from_dict(seqs_4, key), get_data_from_dict(seqs_3, key), get_data_from_dict(seqs_2, key), get_data_from_dict(seqs_1, key) ]
	    normed=True 
        hist.draw_actual_plot(axarr[0,ind], data, "", key.capitalize(), log=log, normed=normed, label=["Cl. by 5", "Cl. by 4", "Cl. by 3", "Cl. by 2", "Cl. by 1"], nbins=nbins)    
        axarr[0,ind].ticklabel_format(axis='x', style='sci', scilimits=(-2,2))

        pconv.add_legend(axarr[0,ind], location="upper right")
    pconv.save_fig(fig, output_prefix, metric, n_to_plot*5, 5, tight=True, size=12) 

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--list_nodes', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--metric', default="metrics", help='name of metric to plot.  To plot all metrics, input metrics')

    args = parser.parse_args()

    main(args.list_nodes, args.output_prefix, args.metric)
