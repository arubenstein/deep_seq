#!/usr/bin/env python

"""Plot degree distribution for various nbunches"""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
import networkx
from networkx.readwrite import json_graph
import json

def main(json_file, output_prefix, nbunch_file):
    
    with open(json_file) as data_file:    
        data = json.load(data_file)

    G = json_graph.node_link_graph(data)

    sequences = seq_IO.read_sequences(nbunch_file) 

    id_seq = networkx.get_node_attributes(G, "sequence")

    seq_id = { seq : node_id for node_id, seq in id_seq.items()}

    nbunch = [ seq_id[seq] for seq in sequences ]

    degrees = networkx.degree(G, nbunch)

    with open("{0}_degree.txt".format(output_prefix), 'w') as o:
        o.write("\n".join([ "{0},{1}".format(id_seq[k], str(d)) for k,d in degrees.items() ]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--json_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--nbunch_file', help='file of sequences if filtering on nbunch is required')

    args = parser.parse_args()

    main(args.json_file, args.output_prefix, args.nbunch_file)
