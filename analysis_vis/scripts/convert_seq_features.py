#!/usr/bin/env python

"""Convert list of sequences into their equivalent SVM features 20*i+n"""
import argparse
from general_seq import seq_IO
from general_seq import conv
import os

AA_ALPHA = { "A" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8,
                 "K" : 9, "L" : 10, "M" : 11, "N" : 12, "P" : 13, "Q" : 14, "R" : 15, "S" : 16,
                 "T" : 17, "V" : 18, "W" : 19, "Y" : 20 }

def conv_char(ch):
    l = [0] * 20
    l[AA_ALPHA[ch]-1] = 1
    return l

def conv_binary_seq(sequences):
    sequence_features = {}
    for seq in sequences:
        sequence_features[seq] = [ str(c) for ch in seq for c in conv_char(ch) ]
    return sequence_features

def conv_alpha_seq(sequences):
    sequence_features = {}
    for seq in sequences:
        sequence_features[seq] = [ str(20*i+AA_ALPHA[seq[i-1]]) for i in xrange(1,len(seq)+1) ]
    return sequence_features

def main(list_sequence_names, conversion_type="alpha"):    

    if list_sequence_names == "random":
        sequences = conv.generate_random_seqs(5) #used 5 as current length because that's my current use for it, can be customized later
    else:
        sequences = seq_IO.read_sequences(list_sequence_names)
    sequence_features = {}

    if conversion_type == "alpha":
        sequence_features = conv_alpha_seq(sequences)
    elif conversion_type == "binary":
        sequence_features = conv_binary_seq(sequences)
    else:
	raise Exception("Conversion type must be binary or alpha")

    base = os.path.splitext(list_sequence_names)[0]

    outfile = '%s_sequence_features_%s.csv' % (base,conversion_type)

    out = open(outfile,"w")
    #out.write(','.join(["Sequence"] + [ str(i) for i in xrange(1,len(sequences[0])+1)] ))
    #out.write("\n")
    for seq, features in sorted(sequence_features.items()):
	out.write(",".join( [seq] + ( features ) ))
        #out.write(",".join( features ) )
        out.write("\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', help="text file which contains sequences")
    parser.add_argument ('--conversion_type', help="binary or alpha features")

    args = parser.parse_args()

    main(args.sequence_list, args.conversion_type)
