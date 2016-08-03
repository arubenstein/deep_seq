#!/usr/bin/env python

"""Convert list of sequences into their equivalent SVM features 20*i+n"""
import argparse
from general_seq import seq_IO
import os

def main(list_sequence_names):    

    sequences = seq_IO.read_sequences(list_sequence_names)
    sequence_features = {}

    AA_alpha = { "A" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, 
                 "K" : 9, "L" : 10, "M" : 11, "N" : 12, "P" : 13, "Q" : 14, "R" : 15, "S" : 16, 
                 "T" : 17, "V" : 18, "W" : 19, "Y" : 20 }

    for seq in sequences:
        sequence_features[seq] = [ str(20*i+AA_alpha[seq[i-1]]) for i in xrange(1,len(seq)+1) ]

    base = os.path.splitext(list_sequence_names)[0]

    outfile = '%s_sequence_features.csv' % (base)

    out = open(outfile,"w")
    out.write(','.join(["Sequence"] + [ str(i) for i in xrange(1,len(sequences[0])+1)] ))
    out.write("\n")
    for seq in sorted(sequences): 
        out.write(",".join( [seq] + (sequence_features[seq] ) ))
        out.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', help="text file which contains sequences")

    args = parser.parse_args()

    main(args.sequence_list)
