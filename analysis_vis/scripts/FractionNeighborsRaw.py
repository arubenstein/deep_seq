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
from plot import conv as pconv
from plot import hist 

def main(list_sequence_names, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename) 
        list_sequences.append(sequences)
        labels.append(label)

    cleaved_ind = labels.index("CLEAVED")
    middle_ind = labels.index("MIDDLE")
    uncleaved_ind = labels.index("UNCLEAVED")

    fracs_cleaved = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], list_sequences[middle_ind], list_sequences[cleaved_ind])
    fracs_uncleaved = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], list_sequences[middle_ind], list_sequences[uncleaved_ind])
    fracs_middle = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], list_sequences[middle_ind], list_sequences[middle_ind])

    with open("{0}_cleaved.csv".format(output_prefix),'w') as f:
        f.write("Sequence,Frac_Cleaved,Frac_Middle,Frac_Uncleaved\n")
        f.write("".join([ "{0},{1},{2},{3}\n".format(k,str(v[0]),str(v[1]),str(v[2])) for k, v in fracs_cleaved.items() ]))

    with open("{0}_middle.csv".format(output_prefix),'w') as f:
        f.write("Sequence,Frac_Cleaved,Frac_Middle,Frac_Uncleaved\n")
        f.write("".join([ "{0},{1},{2},{3}\n".format(k,str(v[0]),str(v[1]),str(v[2])) for k, v in fracs_middle.items() ]))

    with open("{0}_uncleaved.csv".format(output_prefix),'w') as f:
        f.write("Sequence,Frac_Cleaved,Frac_Middle,Frac_Uncleaved\n")
        f.write("".join([ "{0},{1},{2},{3}\n".format(k,str(v[0]),str(v[1]),str(v[2])) for k, v in fracs_uncleaved.items() ]))        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)
