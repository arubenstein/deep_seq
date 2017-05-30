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

    total = float(len(cleaved_dna))

    source_dna = dna_conv.rev_translate(source)

    neighbors_set = set.union(*[dna_conv.gen_hamdist_one(seq) for seq in source_dna])
    cl_neighbors = neighbors_set.intersection(cleaved_dna)

    print "Found Fracs for Cleaved Sequences at: {0}".format(datetime.datetime.now())    

    print "Fracs are: {0}".format(float(len(cl_neighbors))/len(neighbors_set))

#    with open("{0}_{1}.csv".format(output_prefix,source),'w') as f:
#       f.write("\n".join([ "{0},{1}".format(str(x),str(y)) for x, y in zip(list_x,list_y) ]))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--source', help='sequence to start from')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix, args.source)
