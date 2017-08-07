#!/usr/bin/env python

"""Convert list of sequences into their equivalent SVM features 20*i+n"""
import argparse
from general_seq import seq_IO
from general_seq import conv
import os

def main(sequence_list, canonical_seq_list, known_cleaved):    

    sequences = seq_IO.read_sequences(sequence_list, additional_params=True)

    canonical_seqs = seq_IO.read_sequences(canonical_seq_list)

    known_cleaved_list = seq_IO.read_sequences(known_cleaved)

    base = os.path.splitext(sequence_list)[0]

    cleaved_seqs = [ (s[0],s[1],s[2],min([conv.hamdist(s[0],c) for c in canonical_seqs])) for s in sequences if s[1] == 'CLEAVED' and s[2] > 2.0 and s[0] not in known_cleaved_list]
    uncleaved_seqs = [ (s[0],s[1],s[2],min([conv.hamdist(s[0],c) for c in canonical_seqs])) for s in sequences if s[1] == 'UNCLEAVED' and s[2] < -2.0 and s[0] not in known_cleaved_list]

    cl_s_dist = [ s[2] for s in cleaved_seqs]
    uncl_s_dist = [s[2] for s in uncleaved_seqs]

    print max(cl_s_dist)
    print min(uncl_s_dist)

    cleaved_seqs_low_ham = sorted(cleaved_seqs, key=lambda x: (x[3], -x[2]))[0:4]
    cleaved_seqs_hi_ham = sorted(cleaved_seqs, key=lambda x: (-x[3], -x[2]))[0:4]
    uncleaved_seqs_low_ham = sorted(uncleaved_seqs, key=lambda x: (x[3], x[2]))[0:4]
    uncleaved_seqs_hi_ham = sorted(uncleaved_seqs, key=lambda x: (-x[3], x[2]))[0:4]

    outfile = '%s_selected.csv' % (base)

    out = open(outfile,"w")
    out.write("Cleaved_seqs_low_hamming_distance\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in cleaved_seqs_low_ham ] )) 
    out.write("\nCleaved_seqs_high_hamming_distance\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in cleaved_seqs_hi_ham ] ))
    out.write("\nUncleaved_seqs_low_hamming_distance\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in uncleaved_seqs_low_ham ] ))
    out.write("\nUncleaved_seqs_high_hamming_distance\n")
    out.write("\n".join( [ ",".join(map(str,s)) for s in uncleaved_seqs_hi_ham ] ))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', help="text file which contains sequences,labels,distances")
    parser.add_argument ('--canonical_seq_list', help="list of canonical sequences")
    parser.add_argument ('--known_cleaved', help="list of known cleaved sequences")

    args = parser.parse_args()

    main(args.sequence_list, args.canonical_seq_list, args.known_cleaved)
