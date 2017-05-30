#!/usr/bin/env python

"""Find fraction of shells around all sequences."""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
import datetime
from general_seq import dna_conv

def find_fraction_for_shell(list_shell, adj_list, total):
    total_fraction = 0.0
    new_neighbors = set()

    new_neighbors = set.union(*[adj_list[seq]["CLEAVED"] for seq in list_shell])

    print "Found Fracs at: {0}".format(datetime.datetime.now())

    return len(new_neighbors)/total, new_neighbors

def main(list_sequence_names, output_prefix, source):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename) 
        list_sequences.append(sequences)
        labels.append(label)

    print "Read in Sequences at: {0}".format(datetime.datetime.now())

    cleaved_ind = labels.index("CLEAVED")
    uncleaved_ind = labels.index("UNCLEAVED")

    cleaved_dna = set([ dna_seq for aa_seq in list_sequences[cleaved_ind] for dna_seq in dna_conv.rev_translate(aa_seq) ])

    print "Converted to dna at: {0} for # sequences: {1}".format(datetime.datetime.now(), len(cleaved_dna))

    adj_list_cleaved = dna_conv.adj_list_cleaved(cleaved_dna, cleaved_dna)

    print "Created Adj List and Fracs at: {0}".format(datetime.datetime.now())

    total = float(len(cleaved_dna))

    list_x = [0]
    list_y = [1/total]

    new_neighbors = [source]

    for x in xrange(1,3):
        frac, new_neighbors = find_fraction_for_shell(new_neighbors, adj_list_cleaved, total)
        list_x.append(x)
        list_y.append(frac)

    print "Found Fracs for Cleaved Sequences at: {0}".format(datetime.datetime.now())    

    with open("{0}_{1}.csv".format(output_prefix,source),'w') as f:
        f.write("\n".join([ "{0},{1}".format(str(x),str(y)) for x, y in zip(list_x,list_y) ]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--source', help='sequence to start from')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix, args.source)
