#!/usr/bin/env python

"""Plot all graph metrics as histograms"""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
import networkx
from networkx.readwrite import json_graph
import json

def main(json_file, output_prefix, metric):
    
    with open(json_file) as data_file:    
        data = json.load(data_file)

    G = json_graph.node_link_graph(data)

    metrics = {}

    metrics["degree"] = networkx.degree(G)
    #metrics["closeness"] = networkx.closeness_centrality(G).values()
    #TODO: add any other metrics here using a similar format to above line.

    if metric != "metrics":
	labels_to_plot = [metric]
    else:
	labels_to_plot = metrics.keys()

    for ind, key in enumerate(labels_to_plot):
        with open("{0}_{1}.txt".format(output_prefix, key), 'w') as o:
            o.write("\n".join(metrics[key]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--json_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--metric', default="metrics", help='name of metric to plot.  To plot all metrics, input metrics')

    args = parser.parse_args()

    main(args.json_file, args.output_prefix, args.metric)
