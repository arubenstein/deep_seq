#!/usr/bin/env python

"""Create edges and nodes from a list of sequences that are a given hamming distance apart"""
import itertools
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
    list_fit = [ np.random.choice([0,0.5,1], p=[0.48,0.28,0.24]) for i in list_inter ]
    #list_fit = [ dict_fitnesses.get(i) for i in list_inter ]
    return list_inter, list_fit

def calc_epi(list_fit, ending_fit):
    ind = sum([f - 1.0 for f in list_fit ])
    if ind < -1.0:
        ind = -1.0
    elif ind > 0.0:
        ind = 1.0

    epi = (ending_fit - 1.0) - ind 
    
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

def main(list_sequence_names, output_prefix):
    
    list_sequences = [] #list of list of sequences, where each item represents a label 
    extended_list_sequences = [] #flat list of sequences
    labels = [] #labels for list_sequences


    for [filename, label] in list_sequence_names:
        sequences = seq_IO.read_sequences(filename, additional_params=True, ind_type={1:float, 2:float})
	print sequences[0:10]
        list_sequences.append(sequences)
        extended_list_sequences.extend(sequences[:])
        labels.append(label)
    
    print len(extended_list_sequences)
    dict_seq_fit = { seq : fitness for (seq, fitness, ratio) in extended_list_sequences }
    dict_seq_ratio = { seq : ratio for (seq, fitness, ratio) in extended_list_sequences }
    print len(dict_seq_fit)
    
    epi = {}
    outfile_epi = '%s_epi_double.csv' % (output_prefix)
    epi_double_out = open(outfile_epi,"w")
    outfile_epi = '%s_epi.csv' % (output_prefix)
    epi_out = open(outfile_epi,"w")

    mut_func = { "Both_Functional" : [], "Both_Nonfunctional" : [], "One_Functional" : [] }
    mut_nonfunc = { "Both_Functional" : [], "Both_Nonfunctional" : [], "One_Functional" : [] }

    prod = itertools.product(list_sequences[labels.index("CLEAVED")], extended_list_sequences)
    pairs = set()
    counter = 0
    counter_prod = 0
    for x, y in prod:
	counter_prod += 1
        if x[0] != y[0]:
	   counter += 1
           pairs.add(frozenset((x, y)))
    print counter_prod
    print len(pairs)
    print counter
    print "done making set"
    for can, seq_fit in pairs: 
	canonical_seq = can[0]
        seq = seq_fit[0]
        fit = seq_fit[1] 
        mut_dict = mut_func if fit == 1 else mut_nonfunc
            
        dist = conv.hamdist(canonical_seq,seq)
        if dist <= 1:
            continue 
        list_inter, list_fit = get_inter_fitness(canonical_seq, seq, dict_seq_fit)
        if None not in list_fit:
            if dist == 2:
                sum_fit = sum(list_fit)
                if sum_fit > 1.95:
                    mut_dict["Both_Functional"].append((canonical_seq, seq, list_inter, list_fit))
                elif sum_fit < 0.05:
                    mut_dict["Both_Nonfunctional"].append((canonical_seq, seq, list_inter, list_fit))
                else: #either one uncleaved or one middle
		    mut_dict["One_Functional"].append((canonical_seq, seq, list_inter, list_fit))
            epi[(canonical_seq,seq)] = (calc_epi(list_fit, fit),fit,list_fit,list_inter)
    print "done calc epi" 
    '''epi_double_out.write("Starting,Starting_Ratio,Ending,Ending_Ratio,Status_Ending,Status_Intermediates,Inter1_Seq,Inter1_Fit,Inter1_Ratio,Inter2_Seq,Inter2_Fit,Inter2_Ratio\n")
    for label, list_muts in mut_func.items():
        for (can, seq, list_inter, list_fit) in list_muts:
            epi_double_out.write("{start},{start_ratio},{end},{end_ratio},End_Cleaved,{label},{data}\n".format(label=label,start=can,end=seq,
					start_ratio=dict_seq_ratio[can],end_ratio=dict_seq_ratio[seq],
					data = ",".join([ "{0},{1},{2}".format(seq,fitness_to_str(fit),dict_seq_ratio[seq]) for seq,fit in zip(list_inter,list_fit)])) )
    for label, list_muts in mut_nonfunc.items():
        for (can, seq, list_inter, list_fit) in list_muts:
            epi_double_out.write("{start},{start_ratio},{end},{end_ratio},End_Uncleaved,{label},{data}\n".format(label=label,start=can,end=seq,
                                        start_ratio=dict_seq_ratio[can],end_ratio=dict_seq_ratio[seq],
                                        data = ",".join([ "{0},{1},{2}".format(seq,fit,dict_seq_ratio[seq]) for seq,fit in zip(list_inter,list_fit)])) ) 
    '''
    epi_out.write("Starting,Starting_Ratio,Ending,Ending_Ratio,Ending_Fitness,Epistasis,List_Seqs_Fitnesses_Ratios_Intermediates\n")
    epi_out.write("\n".join(["{0},{1},{2},{3},{4},{5},{6}".format(can,dict_seq_ratio[can],seq,dict_seq_ratio[seq],fitness_to_str(fit),e,
			",".join([ "{0},{1},{2}".format(s,fitness_to_str(f),dict_seq_ratio[s]) for f,s in zip(list_fit,list_inter)])) for (can,seq), (e,fit,list_fit,list_inter) in epi.items()] ) ) 
    epi_out.close()
    epi_double_out.close()
    print "done writing epi"
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_list', '-d', nargs=2, action='append', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_list, args.output_prefix)
