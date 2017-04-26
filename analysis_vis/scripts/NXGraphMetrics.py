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
from networkx.readwrite import json_graph
import json

def main(json_file, output_prefix, metric):
    
    with open(json_file) as data_file:    
        data = json.load(data_file)

    G = json_graph.node_link_graph(data)

    metrics = {}

    #metrics["degree"] = degree(G)
    metrics["closeness"] = closeness_centrality(G).values()
    #TODO: add any other metrics here using a similar format to above line.
    sequences = {}    	

    cleaved_seq = { key : val for key, val in sequences.items() if val["type"] == "CLEAVED" }

    if metric != "metrics":
	labels_to_plot = [metric]
    else:
	labels_to_plot = metrics.keys()
    n_to_plot = len(labels_to_plot)
    fig, axarr = pconv.create_ax(n_to_plot, 1, shx=False, shy=False)

    nbins = 20    

    for ind, key in enumerate(labels_to_plot):
	normed = True
        hist.draw_actual_plot(axarr[0,ind], metrics["key"], "", key.capitalize(), normed=normed, nbins=nbins)    
        axarr[0,ind].ticklabel_format(axis='x', style='sci', scilimits=(-2,2))

        #pconv.add_legend(axarr[0,ind], location="middle right")
    pconv.save_fig(fig, output_prefix, "metrics", n_to_plot*5, 5, tight=True, size=12) 

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--json_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--metric', default="metrics", help='name of metric to plot.  To plot all metrics, input metrics')

    args = parser.parse_args()

    main(args.json_file, args.output_prefix, args.metric)
