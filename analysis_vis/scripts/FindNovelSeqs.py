#!/usr/bin/env python

"""Find sequences that are a given hamming distance or chemically similar to a list of canonical sequences"""
import argparse
from general_seq import conv
from general_seq import seq_IO
import glob
import os

def chem_sim(seq1, seq2):
    group1 = "LIV"
    group2 = "TS"
    group3 = "RK"
    group4 = "CM"
    group5 = "DE" 
    
    for ch1, ch2 in zip(seq1, seq2):
        if ch1 != ch2:
            if all([ch1 in group1, ch2 in group1]) or all([ch1 in group2, ch2 in group2]) or all([ch1 in group3, ch2 in group3]) or all([ch1 in group4, ch2 in group4]) or all([ch1 in group5, ch2 in group5]):
                continue
            else:
	        return False

    return True 

def find_seqs_less_than(can, sequences, set_sequences, hamm_dist):
    if hamm_dist == -1:
        set_sequences = set_sequences.union([ seq for seq in sequences if chem_sim(seq, can) ])
    else:
        set_sequences = set_sequences.union([ seq for seq in sequences if conv.hamdist(seq,can) <= hamm_dist ])
    return set_sequences

def find_seqs_more_than(can, sequences, set_sequences, hamm_dist):
    if hamm_dist == -1: 
        set_sequences = set_sequences.intersection([ seq for seq in sequences if chem_sim(seq, can) ])
    else:
        set_sequences = set_sequences.intersection([ seq for seq in sequences if conv.hamdist(seq,can) > hamm_dist ])
    return set_sequences

def find_seqs_more_than_first(can, sequences, set_sequences, hamm_dist):
    if hamm_dist == -1:
        set_sequences = set([ seq for seq in sequences if chem_sim(seq, can) ])
    else:
        set_sequences = set([ seq for seq in sequences if conv.hamdist(seq,can) > hamm_dist ])
    return set_sequences

def main(input_file, canonical_file, output_prefix, hamm_dist, less_than, more_than):

    set_sequences = set()
    canonical_sequences = [] 
    canonical_sequences = seq_IO.read_sequences(canonical_file)
    sequences = seq_IO.read_sequences(input_file) 
    for ind, can in enumerate(canonical_sequences):
        if less_than and more_than:
            raise ValueError('Cannot set both --less_than and --more_than')
	elif less_than:
	    set_sequences = find_seqs_less_than(can, sequences, set_sequences, hamm_dist)
        elif more_than and ind == 0:
	    set_sequences = find_seqs_more_than_first(can, sequences, set_sequences, hamm_dist)
	elif more_than:
	    set_sequences = find_seqs_more_than(can, sequences, set_sequences, hamm_dist)
        else:
	    raise ValueError('Cannot have both --less_than and --more_than as false')

    less_v_more = "less" if less_than else "more"

    outfile_canon = '%scanonical_sim_cleaved_%s_%d.csv' % (output_prefix, less_v_more, hamm_dist)

    with open(outfile_canon, "w") as canon_out:
        canon_out.write('\n'.join(set_sequences))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--input_file', '-d', help="input cleaved sequence file")

    parser.add_argument ('--canonical_file', help='file that contains canonical sequences')

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--hamm_dist', type=int, help='Maximum hamming dist from canonical_seq')

    parser.add_argument ('--less_than', action='store_true', default=False, help='Look for sequences that are <= hamm_dist from any canonical sequence')
    parser.add_argument ('--more_than', action='store_true', default=False, help='Look for sequences that are > hamm_dist from all canonical sequences') #this and above option should be mutually exclusive but this hasn't been enforced in the parser just in the main function

    args = parser.parse_args()

    main(args.input_file, args.canonical_file, args.output_prefix, args.hamm_dist, args.less_than, args.more_than)
