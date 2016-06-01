#!/usr/bin/env python

from scipy.stats.stats import pearsonr
import glob
import os
import sys
import argparse
def read_counts(counts_filename):
    with open(counts_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = { line.split()[1] : float(line.split()[8]) for line in lines if '*' not in line.split()[1] }

    return lines_proc

def read_ratios(ratios_filename):
    with open(ratios_filename) as f:
	lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = { line.split()[1] : float(line.split()[7]) for line in lines if '*' not in line.split()[1] }
    return lines_proc

def combine_counts_ratios(counts, ratios, low_cutoff, high_cutoff):
    merged = { key : (counts[key],ratios[key]) for key in counts if key in ratios and counts[key] >= low_cutoff and counts[key] <= high_cutoff }
    #merged = { key : (counts[key],ratios[key]) for key in counts if key in ratios }
    return merged

def find_coeff_pval(merged):

    c_list = [ c for k,(c,r) in sorted(merged.items()) ]
    r_list = [ r for k,(c,r) in sorted(merged.items()) ]
    coeff, pval = pearsonr(c_list, r_list)
    return coeff, pval

def process_dir(dirname, unsel):
    counts_fn = dirname + '/counts_' + unsel + '*_PRO_qc'
    ratios_fn = dirname + '/ratios_*_PRO_qc'

    c_fn = glob.glob(counts_fn)[0]
    r_fn = glob.glob(ratios_fn)[0]
    
    c = read_counts(c_fn)
    r = read_counts(r_fn)
    
    for i in xrange(1,20):
        m = combine_counts_ratios(c, r, i, i+9)
        coeff, pval = find_coeff_pval(m) 
	print i, coeff, pval

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir', '-d', help="directory for counts and ratios files")

    parser.add_argument('--unsel', help='name of unsel i.e. Sample2')

    args = parser.parse_args()

    process_dir(args.input_dir, args.unsel )
    
