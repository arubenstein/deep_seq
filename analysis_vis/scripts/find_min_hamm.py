#!/usr/bin/env python

"""Convert list of sequences into their equivalent SVM features 20*i+n"""
import argparse
from general_seq import seq_IO
from general_seq import conv
import os

def main(sequence_list, trained_cleaved, trained_uncleaved):    

    sequences = seq_IO.read_sequences(sequence_list, additional_params=True)

    trained_cleaved_list = seq_IO.read_sequences(trained_cleaved)

    trained_uncleaved_list = seq_IO.read_sequences(trained_uncleaved)

    base = os.path.splitext(sequence_list)[0]

    cleaved_seqs = [ (s[0],s[1],min([conv.hamdist(s[0],c) for c in trained_cleaved_list])) for s in sequences if s[1] == 'CLEAVED' ]
    uncleaved_seqs = [ (s[0],s[1],min([conv.hamdist(s[0],c) for c in trained_uncleaved_list])) for s in sequences if s[1] == 'UNCLEAVED' ]

    outfile = '%s_selected_hamm.csv' % (base)

    out = open(outfile,"w")
    out.write("Cleaved_seqs\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in cleaved_seqs ] )) 
    out.write("\nUncleaved_seqs\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in uncleaved_seqs] ))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', help="text file which contains sequences,labels")
    parser.add_argument ('--trained_cleaved', help="list of trained cleaved sequences")
    parser.add_argument ('--trained_uncleaved', help="list of trained uncleaved sequences")

    args = parser.parse_args()

    main(args.sequence_list, args.trained_cleaved, args.trained_uncleaved)
