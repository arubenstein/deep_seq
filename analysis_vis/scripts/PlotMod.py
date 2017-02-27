#!/usr/bin/env python

"""Plot all graph metrics as histograms"""
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
from collections import Counter

def get_data_from_dict( sequence_dict, label ):
    return [ val[label] for key, val in sequence_dict.items() ]

def main(list_nodes, output_prefix):
    
    sequences = seq_IO.read_sequences(list_nodes, additional_params=True, header=True)

    mod = get_data_from_dict( sequences, "modularity_class" )

    count_mods = Counter(mod)
    total = float(sum(count_mods.values()))
    freq_mods = [ key for key, val in count_mods.items() if val/total > 0.01 ]

    for mod_class in freq_mods:
	nodes = [ key for key, val in sequences.items() if val["modularity_class"] == mod_class ]
        with open(output_prefix + "_{0}.txt".format(mod_class), 'w') as f:
	    f.write('\n'.join(nodes))    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--list_nodes', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.list_nodes, args.output_prefix)
