#!/usr/bin/env python

"""Find fraction of shells around all sequences."""
import itertools
import sys
import operator
import argparse
from general_seq import conv
from general_seq import seq_IO
from plot import conv as pconv
from plot import hist 
import datetime

def find_fraction_for_shell(list_shell, adj_list, fracs):
    total_fraction = 0.0
    new_neighbors = []

    for seq in list_shell:
        new_neighbors += adj_list[seq]["CLEAVED"] + adj_list[seq]["UNCLEAVED"]
    for n in new_neighbors:
        total_fraction += fracs[n][0]

    return total_fraction/len(new_neighbors), new_neighbors

def main(list_sequence_names, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename) 
        list_sequences.append(sequences)
        labels.append(label)

    print "Read in Sequences at: {0}".format(datetime.datetime.now())

    cleaved_ind = labels.index("CLEAVED")
    #middle_ind = labels.index("MIDDLE")
    uncleaved_ind = labels.index("UNCLEAVED")

    adj_list_cleaved = conv.adj_list(set(list_sequences[cleaved_ind]), set(list_sequences[uncleaved_ind]), set(), set(list_sequences[cleaved_ind]), ignore_middle=False)
    adj_list_uncleaved = conv.adj_list(set(list_sequences[cleaved_ind]), set(list_sequences[uncleaved_ind]), set(), set(list_sequences[uncleaved_ind]), ignore_middle=False)

    fracs_cleaved = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], [], list_sequences[cleaved_ind], ignore_middle=True)
    fracs_uncleaved = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], [], list_sequences[uncleaved_ind], ignore_middle=True)
    #fracs_middle = conv.fraction_neighbors_all(list_sequences[cleaved_ind], list_sequences[uncleaved_ind], list_sequences[middle_ind], list_sequences[middle_ind])

    print "Created Adj List and Fracs at: {0}".format(datetime.datetime.now())

    adj_list = adj_list_cleaved + adj_list_uncleaved
    fracs = fracs_cleaved + fracs_uncleaved

    fracs_per_seq = {}

    for seq in list_sequences[cleaved_ind]:
	new_neighbors = [seq]
	fracs_per_seq[seq] = []
        for x in xrange(0,4):
            frac, new_neighbors = find_fraction_for_shell(new_neighbors, adj_list, fracs)
	    fracs_per_seq[seq].append(frac)

    print "Found Fracs for Cleaved Sequences at: {0}".format(datetime.datetime.now())    

    with open("{0}_cleaved.csv".format(output_prefix),'w') as f:
        f.write("Sequence,1,2,3,4\n")
        f.write("".join([ "{0},{1},{2},{3},{4}\n".format(k,str(v[0]),str(v[1]),str(v[2]),str(v[3])) for k, v in fracs_per_seq.items() ]))

    #with open("{0}_middle.csv".format(output_prefix),'w') as f:
    #    f.write("Sequence,Frac_Cleaved,Frac_Middle,Frac_Uncleaved\n")
    #    f.write("".join([ "{0},{1},{2},{3}\n".format(k,str(v[0]),str(v[1]),str(v[2])) for k, v in fracs_middle.items() ]))

    #with open("{0}_uncleaved.csv".format(output_prefix),'w') as f:
    #    f.write("Sequence,Frac_Cleaved,Frac_Middle,Frac_Uncleaved\n")
    #    f.write("".join([ "{0},{1},{2},{3}\n".format(k,str(v[0]),str(v[1]),str(v[2])) for k, v in fracs_uncleaved.items() ]))        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)
