#!/usr/bin/env python

"""Read in a list of edges and nodes.  For each source node, randomly retarget it to any target node."""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
import numpy as np

def conv_fitness_label(fitness):
    if fitness == 2:
        return "CLEAVED"
    elif fitness == 1.5:
        return "MIDDLE"
    else:
	return "UNCLEAVED"

def main(list_sequence_names, hamming_dist, output_prefix, canonical_file):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences

    #canonical_seqs = seq_IO.read_sequences(canonical_file)
    canonical_seqs = ['DEMEE']

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float})
        new_seqs = [ (seq,fitness,min([ conv.hamdist(seq,can) for can in canonical_seqs ]) <= 2) for seq,fitness in sequences ] 
        list_sequences.append(new_seqs)
        extended_list_sequences.extend(new_seqs[:])
        labels.append(label)

    outfile_nodes = '%s_nodes.csv' % (output_prefix)

    edges = [(seq2,seq) for seq,seq2 in itertools.combinations(extended_list_sequences,2) if conv.hamdist(seq2[0],seq[0]) == hamming_dist ]

    tallies = { 2 : {2:0,1.5:0,1:0}, 1.5 : {2:0,1.5:0,1:0}, 1 : {2:0,1.5:0,1:0} }
    

    for edge in edges:
        tallies[edge[0][1]][edge[1][1]] += 1

    frequencies = { 2 : {}, 1.5 : {}, 1 : {} }

    for source, tallies_dict in tallies.items():
        n_tallies = float(sum(tallies_dict.values()))
        frequencies[source] = { k : v/n_tallies for k, v in tallies_dict.items() }

    new_edges = []

    for edge in edges:
	fitness_source = edge[0][1]
        fitness_target = np.random.choice([2,1.5,1],p=[frequencies[fitness_source][2],frequencies[fitness_source][1.5],frequencies[fitness_source][1]])   
 	seqs = list_sequences[labels.index(conv_fitness_label(fitness_target))]
        new_edges.append((edge[0],seqs[np.random.randint(0,len(seqs)-1)]))

    edges = new_edges
      
    for canonical_seq in canonical_seqs: 
        outfile_edges = '%s_%s_edges.csv' % (output_prefix, canonical_seq)
        edges_out = open(outfile_edges,"w")
        edges_out.write("Source,Target,Weight\n")
	print canonical_seq
        for ([seq1,fit1,can1],[seq2,fit2,can2]) in edges:
            dist_seq1 = conv.hamdist(canonical_seq, seq1)
            dist_seq2 = conv.hamdist(canonical_seq, seq2)
            fit_lower = fit1 if dist_seq1 < dist_seq2 else fit2
            fit_upper = fit2 if dist_seq1 < dist_seq2 else fit1
            fit_upper = fit_upper if fit_upper > 0 else 0.001
            seq_lower = seq1 if dist_seq1 < dist_seq2 else seq2
            seq_upper = seq2 if dist_seq1 < dist_seq2 else seq1        
	    out_str = "{0},{1},{2}\n".format(seq_lower,seq_upper,fit_lower/float(fit_upper))
	    edges_out.write(out_str) #does this have the correct directionality?
	edges_out.close()

    already_written_nodes = []
   
    nodes_out = open(outfile_nodes,"w")
    nodes_out.write("Id,Label,Type,Fitness,Canonical\n")
    for seqs,label in zip(list_sequences,labels):
        nodes_out.write("\n".join("{0},{0},{1},{2},{3}".format(x, label, fitness,can) for (x,fitness,can) in seqs if x not in already_written_nodes))
        already_written_nodes.extend([ s[0] for s in seqs])
        nodes_out.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--hamming_dist', default=2, type=int, help='hamming distance to use for calculating edges')

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--canonical_file', help='file of canonical_sequences')

    args = parser.parse_args()

    main(args.sequence_list, args.hamming_dist, args.output_prefix, args.canonical_file)
