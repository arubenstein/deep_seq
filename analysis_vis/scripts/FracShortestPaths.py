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
import os

def main(json_file, output_prefix, novel_seqs_file, canonical_file):

    print "Started Script: {0}".format(datetime.datetime.now())
    
    with open(json_file) as data_file:    
        data = json.load(data_file)

    G = json_graph.node_link_graph(data, directed=False)

    print "Finished Reading in Graph: {0}".format(datetime.datetime.now())

    id_seq = networkx.get_node_attributes(G, "sequence")
    id_status = networkx.get_node_attributes(G, "status")
    seq_id = { seq : node_id for node_id, seq in id_seq.items()}

    print "Created inverse lookup table: {0}".format(datetime.datetime.now())

    novel_seqs = seq_IO.read_sequences(novel_seqs_file)
    canonical_seqs = seq_IO.read_sequences(canonical_file)

    novel_fracs = {}    

    print "Ready to enter loop: {0}".format(datetime.datetime.now())

    for n in novel_seqs:
	novel_fracs[n] = {}
        hamm_dist = sorted([ (conv.hamdist(n,c),c) for c in canonical_seqs ]) 
	min_hamm_dist = hamm_dist[0][0]
        print "Found hamming distances: {0}".format(datetime.datetime.now())

        for hamm, c in hamm_dist:
	    #only analyze min_dist canonical sequences
	    if hamm != min_hamm_dist:
	        continue
	    novel_fracs[n][c] = []
	    #generate list of 5 paths
            #paths = itertools.islice(networkx.all_shortest_paths(G, seq_id[n], seq_id[c]), 5)
            paths = [ networkx.shortest_path(G, seq_id[n], seq_id[c]) ]

            for path in paths:
	        inter_nodes = path[1:-1]
                novel_fracs[n][c].append(float(sum([ 1 for node_id in inter_nodes if id_status[node_id] == "UNCLEAVED" ]))/len(inter_nodes))
    
    base_n_file = os.path.basename(os.path.splitext(novel_seqs_file)[0])
    base_c_file = os.path.basename(os.path.splitext(canonical_file)[0])

    with open("{0}_frac_paths_{1}_{2}.txt".format(output_prefix, base_n_file, base_c_file), 'w') as o:
        for n, c_dict in novel_fracs.items():
	    for c, fracs_list in c_dict.items():
                o.write("{0},{1},".format(n,c))
	        o.write(",".join(map(str,fracs_list)))
		o.write("\n")
	
    print "Output paths: {0}".format(datetime.datetime.now())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--json_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--novel_seqs_file', help='list of sequences to be tested')

    parser.add_argument ('--canonical_file', help='list of canonical sequences')

    args = parser.parse_args()

    main(args.json_file, args.output_prefix, args.novel_seqs_file, args.canonical_file)
