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

def get_inter_fitness(seq, list_dict_fitnesses):
    list_fit =  [ d.get(seq) for d in list_dict_fitnesses ]
    return list_fit

def calc_epi(list_fit, starting_fit, ending_fit):
    ind = sum([f - starting_fit for f in list_fit ])
    if ind < -1.0:
        ind = -1.0
    elif ind > 1.0:
        ind = 1.0

    epi = (ending_fit - starting_fit) - ind 
    
    return epi

def fitness_to_str(fitness):
    if fitness < 0.05:
        fit_str = "UNCLEAVED"
    elif fitness == 0.5:
        fit_str = "MIDDLE"
    elif fitness == 1.0:
        fit_str = "CLEAVED"
    else:
        raise Exception("Fitness must be 1, 10, or 1000")
    return fit_str

def read_sequence_lists( list_sequence_names ):
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences

    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float, 2:float})
        list_sequences.append(sequences)
        extended_list_sequences.extend(sequences[:])
        labels.append(label)

    return list_sequences, extended_list_sequences, labels

def main(start_sequences, inter1_sequences, inter2_sequences, inter3_sequences, end_sequences, inter_muts, output_prefix):
    
    start_list_sequences, start_extended_list_sequences, start_labels = read_sequence_lists( start_sequences )
    end_list_sequences, end_extended_list_sequences, end_labels = read_sequence_lists( end_sequences )
    inter1_list_sequences, inter1_extended_list_sequences, inter1_labels = read_sequence_lists( inter1_sequences)
    inter2_list_sequences, inter2_extended_list_sequences, inter2_labels = read_sequence_lists( inter2_sequences )
    inter3_list_sequences, inter3_extended_list_sequences, inter3_labels = read_sequence_lists( inter3_sequences )

    list_dict_seq_fit = [ { seq : fitness for seq, fitness, ratio in inter1_extended_list_sequences},
			{ seq : fitness for seq, fitness, ratio in inter2_extended_list_sequences},
			{ seq : fitness for seq, fitness, ratio in inter3_extended_list_sequences}]
    end_dict_seq_fit = { seq : fitness for seq, fitness, ratio in end_extended_list_sequences }

    epi = {}
    outfile_epi = '%s_epi.csv' % (output_prefix)
    epi_out = open(outfile_epi,"w")

    for can in start_list_sequences[start_labels.index("CLEAVED")]: 
        canonical = can[0]
	canonical_fit = can[1]
	fit = end_dict_seq_fit.get(canonical)
        if fit is not None:
            list_fit = get_inter_fitness(canonical, list_dict_seq_fit)
            if None not in list_fit:
                epi[canonical] = (calc_epi(list_fit, canonical_fit, fit), canonical_fit, fit,list_fit,inter_muts)

    epi_out.write("Starting,Starting_Fitness,Ending_Fitness,Epistasis,List_Seqs_Fitnesses_Intermediates\n")
    epi_out.write("\n".join(["{0},{1},{2},{3},{4}".format(seq,fitness_to_str(can_fit),fitness_to_str(fit),e,
			",".join([ "{0},{1}".format(s,fitness_to_str(f)) for f,s in zip(list_fit,list_inter)])) for seq, (e,can_fit,fit,list_fit,list_inter) in epi.items()] ) ) 
    epi_out.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--start_sequences', nargs=2, action='append', help="text file which contains WT sequences and the label you want to use for the set")

    parser.add_argument ('--inter1_sequences', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--inter2_sequences', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--inter3_sequences', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--end_sequences', nargs=2, action='append', help="text file which contains triple-mutant sequences and the label you want to use for the set")

    parser.add_argument ('--inter_muts', help="string of mutations of intermediates in correct order")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.start_sequences, args.inter1_sequences, args.inter2_sequences, args.inter3_sequences, args.end_sequences, args.inter_muts, args.output_prefix)
