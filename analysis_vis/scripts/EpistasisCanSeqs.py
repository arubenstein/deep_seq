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

def find_intermediates(starting_seq, ending_seq):
    muts = [ (ch2, ch1!=ch2) for ch1, ch2 in zip(starting_seq, ending_seq) ]
    list_inter = []
    for ind, (mut, is_mut) in enumerate(muts):
        if is_mut:
            list_inter.append(starting_seq[0:ind] + mut + starting_seq[ind+1:])
    return list_inter

def get_inter_fitness(starting_seq, ending_seq, dict_fitnesses):
    list_inter = find_intermediates(starting_seq, ending_seq)
    list_fit = [ dict_fitnesses.get(i) for i in list_inter ]
    return list_fit

def calc_epi(list_fit, ending_fit):
    n_list_fit = []
    for item in list_fit:
        if item == 1000:
            fit = 1
        elif item == 10:
            fit = 0.5
        elif item == 1:
            fit = 0
        n_list_fit.append(fit)
    if ending_fit == 1000:
        fit = 1
    elif ending_fit == 10:
        fit = 0.5
    elif ending_fit == 1:
        fit = 0

    epi = (fit - 1.0) - sum([f - 1.0 for f in n_list_fit ])
    return epi

def main(list_sequence_names, output_prefix, canonical_file):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences


    canonical_seqs = seq_IO.read_sequences(canonical_file)

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float})
        list_sequences.append(sequences)
        extended_list_sequences.extend(sequences[:])
        labels.append(label)

    dict_sequences = { seq : fitness for (seq, fitness) in extended_list_sequences }

    epi = {}

    for canonical_seq in canonical_seqs: 
        mut_func = { "Both_Functional" : [], "Both_Nonfunctional" : [], "One_Functional" : [] }
        mut_nonfunc = { "Both_Functional" : [], "Both_Nonfunctional" : [], "One_Functional" : [] }

        outfile_epi = '%s_%s_epi.csv' % (output_prefix, canonical_seq)
        epi_out = open(outfile_epi,"w")
	print canonical_seq
	epi = {}
        double_mut = [ seq for seq in extended_list_sequences if conv.hamdist(canonical_seq, seq[0]) == 2 ]
        for seq_fit in extended_list_sequences:
            seq = seq_fit[0]
            fit = seq_fit[1] 
            mut_dict = mut_func if fit == 1000 else mut_nonfunc
            list_fit = get_inter_fitness(canonical_seq, seq, dict_sequences)
	    if len(list_fit) <=  1:
                continue
            if all(list_fit):
		if seq_fit in double_mut:
                    
                    sum_fit = sum(list_fit)
	            print sum_fit
                    if sum_fit == 2000:
                        mut_dict["Both_Functional"].append((canonical_seq, seq))
                    elif sum_fit == 0:
                        mut_dict["Both_Nonfunctional"].append((canonical_seq, seq))
                    elif sum_fit == 1000:
                        mut_dict["One_Functional"].append((canonical_seq, seq))
                epi[seq] = (calc_epi(list_fit, fit),list_fit+[fit])

        epi_out.write("Total Double Mutants,%s\n" % (len(double_mut)))

	for label, list_muts in mut_func.items():
            for (can, seq) in list_muts:
                epi_out.write("End Functional,%s,%s,%s\n" % (label,can,seq) )
        for label, list_muts in mut_nonfunc.items():
            for (can, seq) in list_muts:
                epi_out.write("End Functional,%s,%s,%s\n" % (label,can,seq) )	   
	epi_out.write("\n".join(["{0},{1},{2}".format(seq,epi,",".join([str(f) for f in fits])) for seq, (epi,fits) in epi.items()] ) ) 
	epi_out.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--canonical_file', help='file of canonical_sequences')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix, args.canonical_file)
