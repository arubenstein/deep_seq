#!/usr/bin/env python

"""Print out all shortest paths between two nodes"""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
import networkx
from networkx.readwrite import json_graph
import json
import datetime
def main(json_file, output_prefix, source, target):
    
    with open(json_file) as data_file:    
        data = json.load(data_file)

    G = json_graph.node_link_graph(data, directed=False)

    print "Finished Reading in Graph: {0}".format(datetime.datetime.now())

    id_seq = networkx.get_node_attributes(G, "sequence")

    seq_id = { seq : node_id for node_id, seq in id_seq.items()}

    print "Created inverse lookup table: {0}".format(datetime.datetime.now())

    if ',' in target:
        targets = target.split(',')

    for target in targets:
        paths = networkx.all_shortest_paths(G, seq_id[source], seq_id[target])

        with open("{0}_paths_{1}_{2}.txt".format(output_prefix, source, target), 'w') as o:
            for path in paths:
                o.write(",".join( [id_seq[node_id] for node_id in path ] ))
	        o.write("\n")

    print "Output paths: {0}".format(datetime.datetime.now())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--json_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--source', help='source node for path')

    parser.add_argument ('--target', help='target node for path')

    args = parser.parse_args()

    main(args.json_file, args.output_prefix, args.source, args.target)
