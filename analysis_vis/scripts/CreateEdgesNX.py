#!/usr/bin/env python

"""Create edges and nodes from a list of sequences that are a given hamming distance apart"""
import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from general_seq import conv
from general_seq import seq_IO
import json
import datetime

def main(list_sequence_names, hamming_dist, output_prefix, canonical_file):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences

    #canonical_seqs = seq_IO.read_sequences(canonical_file)
    canonical_seqs = ["DEMEE"] #left other code here in case want to try it from all cleaved sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float})
        new_seqs = [ (seq,fitness,min([ conv.hamdist(seq,can) for can in canonical_seqs ]) <= 2) for seq,fitness in sequences ] 
        list_sequences.append(new_seqs)

        extended_list_sequences.extend(new_seqs[:])
	dict_sequences = { n[0] : n for n in new_seqs }
        labels.append(label)

    edges = []
    edges_set = set()
    print "Read in Data: {0}".format(datetime.datetime.now()) 

    for seq, fitness, canonical_like in extended_list_sequences:
        neighbors = conv.gen_hamdist_one(seq)
        edges_set.update([ (seq, n) for n in neighbors if n in dict_sequences ])
	edges += [((seq, fitness, canonical_like), dict_sequences[n] ) for n in neighbors if n in dict_sequences and (n,seq) not in edges_set ]
        print len(edges)
	print len(edges_set)
    print "Generated Edges: {0}".format(datetime.datetime.now())
    print edges[0:10]
    seq_id = { seq[0] : ind for ind, seq in enumerate(extended_list_sequences) } 
  
    nodes = []
    for seqs, label in zip(list_sequences, labels):
        nodes.extend([ { "id" : seq_id[seq[0]], "sequence" : seq[0], "status" : label, "fitness" : seq[1], "canonical_like" : seq[2] } for seq in seqs ])  
   
    print "Generated List of Nodes: {0}".format(datetime.datetime.now()) 
    links = []

    for canonical_seq in canonical_seqs: 
	print canonical_seq
        for ((seq1,fit1,can1),(seq2,fit2,can2)) in edges:
            dist_seq1 = conv.hamdist(canonical_seq, seq1)
            dist_seq2 = conv.hamdist(canonical_seq, seq2)
            fit_lower = fit1 if dist_seq1 < dist_seq2 else fit2
            fit_upper = fit2 if dist_seq1 < dist_seq2 else fit1
            fit_upper = fit_upper if fit_upper > 0 else 0.001
            seq_lower = seq1 if dist_seq1 < dist_seq2 else seq2
            seq_upper = seq2 if dist_seq1 < dist_seq2 else seq1
	    links.append({ "source" : seq_id[seq_lower], "target" : seq_id[seq_upper], "weight" : fit_lower/float(fit_upper) } )        

    print "Generated List of Edges: {0}".format(datetime.datetime.now())

    with open('{0}nodes_edges.json'.format(output_prefix), 'w') as fp:
        json.dump(nodes, fp)
        json.dump(links, fp)

    print "Dumped Nodes and Edges Lists: {0}".format(datetime.datetime.now())    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--hamming_dist', default=2, type=int, help='hamming distance to use for calculating edges')

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--canonical_file', help='file of canonical_sequences')

    args = parser.parse_args()

    main(args.sequence_list, args.hamming_dist, args.output_prefix, args.canonical_file)
