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

def main(input_dir, canonical_file, output_prefix, hamm_dist):

    list_seq_files = glob.glob(os.path.join(input_dir, "*_cleaved.txt"))
    
    dict_sequences = {}
    canonical_sequences = [] 
    canonical_sequences = seq_IO.read_sequences(canonical_file)

    for filename in list_seq_files:
        sequences = seq_IO.read_sequences(filename) 
        for can in canonical_sequences:
            if hamm_dist == -1:
                seq_sim = [ seq for seq in sequences if chem_sim(seq, can) ]
	    else:
       	        seq_sim = [ seq for seq in sequences if conv.hamdist(seq,can) <= hamm_dist ]
	    if seq_sim:
                 dict_sequences[(filename, can)] = seq_sim

    outfile_canon = '%scanonical_sim_cleaved%d.csv' % (output_prefix, hamm_dist)

    canon_out = open(outfile_canon,"w")

    for (filename, can), seqs in dict_sequences.items():
	canon_out.write(filename + "," + can + "," + ','.join(seqs) + "\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--input_dir', '-d', help="input dir that contains cleaved sequence files")

    parser.add_argument ('--canonical_file', help='file that contains canonical sequences')

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--hamm_dist', type=int, help='Maximum hamming dist from canonical_seq')
    args = parser.parse_args()

    main(args.input_dir, args.canonical_file, args.output_prefix, args.hamm_dist)
