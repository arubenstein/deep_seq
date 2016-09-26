#!/usr/bin/env python

import glob
import os
import sys
import argparse

def read_freqs(counts_filename):
    with open(counts_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = dict( (line.split()[1] , float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )

    return lines_proc

def read_ratios(ratios_filename):
    with open(ratios_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    r = dict( (line.split()[1] , float(line.split()[7])) for line in lines if '*' not in line.split()[1] )
    c_unsel = dict( (line.split()[1], float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )
    c_sel = dict( (line.split()[1], float(line.split()[-1])) for line in lines if '*' not in line.split()[1] )
    return r, c_unsel, c_sel

def normalize_list(list_vals, normtype="all"):
    max_val = float(max(list_vals))
    min_val = float(min(list_vals))
    diff = float(max_val-min_val)
    if normtype == "all":
        normed = [ (v-min_val)/diff for v in list_vals ]
    elif normtype == "top":
        normed = [ v/diff for v in list_vals ]
    else:
        raise ValueError
    return normed

def categorize(list_val_tuples_cleaved, list_val_tuples_uncleaved, list_val_tuples_middle):
    categories_dict = {}
    if any(x[0] > 0 for x in list_val_tuples_cleaved.values()) and any(x[0] > 0 for x in list_val_tuples_uncleaved.values()):
        categories_dict["Cleaved and Uncleaved"] = "TRUE"
    elif any(x[0] > 0 for x in list_val_tuples_cleaved.values()) and any(x[0] > 0 for x in list_val_tuples_middle.values()):
        categories_dict["Cleaved and Middle"] = "TRUE"
    elif any(x[0] > 0 for x in list_val_tuples_uncleaved.values()) and any(x[0] > 0 for x in list_val_tuples_middle.values()):
        categories_dict["Uncleaved and Middle"] = "TRUE"
    else:
        categories_dict["Uncleaved"] = ""
        categories_dict["Middle"] = ""
        categories_dict["Cleaved"] = ""

        for sample, x in list_val_tuples_uncleaved.items():
            if x[0] < 0:
	        categories_dict["Uncleaved"] = ""
                break
            elif x[0] > 0:
                categories_dict["Uncleaved"] = categories_dict["Uncleaved"] + (sample)
        for sample, x in list_val_tuples_cleaved.items():
            if x[0] < 0:
                categories_dict["Cleaved"] = ""
                break
            elif x[0] > 0:                
	        categories_dict["Cleaved"] = categories_dict["Cleaved"] + (sample)
        for sample, x in list_val_tuples_middle.items():
            if x[0] < 0:
                categories_dict["Middle"] = ""
                break
            elif x[0] > 0:
                categories_dict["Middle"] = categories_dict["Middle"] + (sample)  
     
    if categories_dict.get("Cleaved and Uncleaved") is None:
        if any(x[0] > 0 for x in list_val_tuples_cleaved.values()) and any(x[0] < 0 for x in list_val_tuples_uncleaved.values()):
            categories_dict["Cleaved Not Uncleaved"] = "TRUE"
        if any(x[0] < 0 for x in list_val_tuples_cleaved.values()) and any(x[0] > 0 for x in list_val_tuples_uncleaved.values()):
            categories_dict["Uncleaved Not Cleaved"] = "TRUE"
    return categories_dict
def process_dir(initial_dir, output_file, datatype):

    if datatype == "nextseq":
        sample_names_dict = { "WT_nextseq" :
                         { "Cleaved" : ["MP02Tr20_Fr3_MP07Tr20_Fr3","MP02Tr20_Fr3_MP72Tr20_Fr3"],
                         "Uncleaved" : ["MP02Tr20_Fr3_MP09Tr20_Fr3","MP02Tr20_Fr3_MP92Tr20_Fr3"],
                         "Middle" : ["MP02Tr20_Fr3_MP08Tr20_Fr3","MP02Tr20_Fr3_MP82Tr20_Fr3"] },
                         "011" : { "Cleaved" : ["MP011Tr20_Fr1_MP012Tr20_Fr1"],
                         "Uncleaved" : ["MP011Tr20_Fr1_MP013Tr20_Fr1"],
                         "Middle" : ["MP011Tr20_Fr1_MP01MTr20_Fr1"] },
                         "021" : { "Cleaved" : ["MP021Tr20_Fr1_MP022Tr20_Fr1"],
                         "Uncleaved" : ["MP021Tr20_Fr1_MP023Tr20_Fr1"],
                         "Middle" : ["MP021Tr20_Fr1_MP02MTr20_Fr1"] },
                         "091" : { "Cleaved" : ["MP091Tr20_Fr1_MP092Tr20_Fr1"],
                         "Uncleaved" : ["MP091Tr20_Fr1_MP093Tr20_Fr1"],
                         "Middle" : ["MP091Tr20_Fr1_MP09MTr20_Fr1"] },
                         "101" : { "Cleaved" : ["MP101Tr20_Fr1_MP102Tr20_Fr1"],
                         "Uncleaved" : ["MP101Tr20_Fr1_MP103Tr20_Fr1"],
                         "Middle" : ["MP101Tr20_Fr1_MP10MTr20_Fr1"] }}
    elif datatype == "miseq":
        sample_names_dict = { "WT_miseq" : { "Cleaved" : ["Sample2_Sample7","Sample2_Sample72"],
                     "Uncleaved" : ["Sample2_Sample9","Sample2_Sample92"],
                     "Middle" : ["Sample2_Sample8","Sample2_Sample82"] } }

    for seq_name, sample_names in sample_names_dict.items():
        seq_values = {}

        #loop thru sample folders.  read in counts_sel, counts_unsel, and ratios per sequence.  Loop thru dict and update seq values with dict. 
        for item in sample_names.values():
            for sample in item:
                ratios_fname = glob.glob(os.path.join(initial_dir, sample, "data", "output", "ratios_*PRO_qc"))[0]
                r, c_unsel, c_sel = read_ratios(ratios_fname)
                for seq, ratio in r.items():
                    if seq_values.get(seq) is None:
                        seq_values[seq] = {}
                    seq_values[seq][sample] = (ratio, c_unsel[seq], c_sel[seq])

        for seq, seq_dict in seq_values.items():
            uncleaved_dict = { sample_name : seq_dict.get(sample_name,(0,0,0)) for sample_name in sample_names["Uncleaved"] }
            cleaved_dict = { sample_name : seq_dict.get(sample_name,(0,0,0)) for sample_name in sample_names["Cleaved"] }
            middle_dict = { sample_name : seq_dict.get(sample_name,(0,0,0)) for sample_name in sample_names["Middle"] }

            seq_values[seq].update(categorize(cleaved_dict, uncleaved_dict, middle_dict))

        with open(output_file + "_" + seq_name + ".csv", 'w') as o:
            s_list = [ s for item in sample_names.values() for s in item ]
            print s_list
            c_list = ["Cleaved and Uncleaved","Cleaved and Middle", "Uncleaved and Middle", "Uncleaved", "Cleaved", "Middle",
                                "Cleaved Not Uncleaved", "Uncleaved Not Cleaved"]
            o.write(','.join(["Sequence"] + [ "{0}-{1},{2},{3}".format(s,"Ratio","Unsel","Sel") for s in s_list ] + c_list ))
            o.write('\n')
            for seq, seq_dict in seq_values.items():
                o.write(seq + ",")
                o.write(','.join([','.join([str(i) for i in seq_dict.get(s,["","",""])]) for s in s_list]))
                o.write(',')
                o.write(','.join([ seq_dict.get(cat,"") for cat in c_list]))
                o.write('\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir', '-d', help="directory for counts and ratios files")

    parser.add_argument('--output_file', help='output_prefix')
    parser.add_argument('--datatype', help='datatype')

    args = parser.parse_args()

    process_dir(args.input_dir, args.output_file, args.datatype)
    
