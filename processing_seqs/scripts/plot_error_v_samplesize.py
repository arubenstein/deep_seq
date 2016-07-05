#!/usr/bin/env python

from scipy.stats.stats import pearsonr
import glob
import os
import sys
import argparse
from plot import conv
from plot import scatterplot
import numpy as np

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

def calc_freq_ratio( freq_file1, freq_file2 ):
    freq_dict1 = read_freqs(freq_file1)
    freq_dict2 = read_freqs(freq_file2)
    freq_ratios_all = [ abs(freq1-freq_dict2[key])/freq1 for key, freq1 in freq_dict1 if key in freq_dict2 ]
    freq_ratio_perc = np.percentile(freq_ratios_all, 75)
    return freq_ratio_perc

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def normalize_list(list_vals):
    max_val = max(list_vals)
    min_val = min(list_vals)
    diff = float(max_val)-min_val

    normed = [ v/diff for v in list_vals ]
    return normed

def plot_curve(ax, x, y, label, title, x_axis, y_axis):
    line.plot_series(ax, (x, y, label), title, x_axis, y_axis)
    ax.plot([0, 1], [1, 0])
    

def process_dir(initial_dir, output_pre):
    #create 3 figures, one for each source of error. for overlap make 4 plots, one for each set of cleaved/uncleaved.  for other two figures, make 3 plots, one for 7-72, one for 8-82, one for 9-92
    fig_all, axarr_all = conv.create_ax(len(dirnames), 3, shx=True, shy=True)

    #almost no error-catching - assumes that all directories from 0-30 are present

    #set up lists
    samplesize = []
    overlap_c_unc = { "MP011Tr20_Fr1_MP012Tr20_Fr1_MP011Tr20_Fr1_MP013Tr20_Fr1": [],
                      "MP021Tr20_Fr1_MP022Tr20_Fr1_MP021Tr20_Fr1_MP023Tr20_Fr1": [],
                      "MP091Tr20_Fr1_MP092Tr20_Fr1_MP091Tr20_Fr1_MP093Tr20_Fr1": [],
                      "MP101Tr20_Fr1_MP102Tr20_Fr1_MP101Tr20_Fr1_MP103Tr20_Fr1": [],
                      "MP02Tr20_Fr3_MP07Tr20_Fr3_MP02Tr20_Fr3_MP09Tr20_Fr3": []}

    freq_freq = { ("MP02Tr20_Fr3_MP07Tr20_Fr3","MP02Tr20_Fr3_MP72Tr20_Fr3") : [],
                  ("MP02Tr20_Fr3_MP08Tr20_Fr3","MP02Tr20_Fr3_MP82Tr20_Fr3") : [],
                  ("MP02Tr20_Fr3_MP09Tr20_Fr3","MP02Tr20_Fr3_MP92Tr20_Fr3") : [] }

    ratios = { "MP07Tr20_Fr3_MP72Tr20_Fr3" : [],
               "MP08Tr20_Fr3_MP82Tr20_Fr3" : [],
               "MP09Tr20_Fr3_MP92Tr20_Fr3" : [] }

    cleaved_lists = [ "MP011Tr20_Fr1_MP012Tr20_Fr1_only.txt", "MP021Tr20_Fr1_MP022Tr20_Fr1_only.txt", "MP091Tr20_Fr1_MP092Tr20_Fr1_only.txt", "MP101Tr20_Fr1_MP102Tr20_Fr1_only.txt", "MP02Tr20_Fr3_MP0772Tr20_Fr3_only.txt" ] 
    

    #for each dirname, glob find all the directories within this dirname
    for threshold in xrange(1,31):
        path_prefix = os.path.join(initial_dir,threshold)
        #todo: check that it exists

        cl_size = [ 0 for _ in cleaved_lists ]
        #find the average number of cleaved sequences for all the cleaved lists (hardcode these)
        for cl in cleaved_lists:
            cl_size.append(file_len(os.path.join(path_prefix,cl)))

        samplesize.append(np.mean(cl_size))

        #do the following for 3 pairs of 7-72 and so on
        for freq1, freq2 in freq_freq.keys():
           freq1_filename = "counts_" + freq1.split("_")[2:] + ".fast_R1_PRO_qc"
           freq2_filename = "counts_" + freq2.split("_")[2:] + ".fast_R1_PRO_qc"
           fr = calc_freq_ratio(os.path.join(path_prefix, freq1, "data", "output", freq1_filename), os.path.join(path_prefix, freq2, "data", "output", freq2_filename))
           freq_freq[(freq1,freq2)].append(fr)

       #collect the ratios for 7-72 - take their abs values and then find the 75th percentile
       for r_name in ratios.keys():
           ratios_fname = glob.glob(os.path.join(path_prefix, r_name, "data", "output", "ratios_*PRO_qc"))[0]
           r, c_unsel, c_sel = read_ratios(ratios_fname)
           r_perc = np.percentile([abs(r_val) for r_val in r], 75)
           ratios[r_name].append(r_perc)

       #find the cleaved_uncleaved overlap.txt file for each of hardcoded cleaved/uncleaved filenames
       for o in overlap_c_unc.keys():
           overlap_c_unc[o].append(file_len(os.path.join(path_prefix,o+"_overlap.txt")))
 
    #plot all figures
    #1. Overlap between cleaved and uncleaved.  Four subplots, one for each set of cleaved/uncleaved
    fig_overlap, axarr_overlap = conv.create_ax(len(overlap_c_unc), 1, shx=True, shy=True)

    for ind, (key, val) in enumerate(overlap_c_unc):
        plot_curve(axarr_overlap[0,ind], val, samplesize, key, key, "Overlap Between Cleaved and Uncleaved", "Sample Size")


    #2. abs(freq7-freq72)/freq7. Three subplots, one for each set of 7-72, 8-82, 9-92

    #3. abs(ratio(7,72)). Three subplots, one for each set of 7-72, 8-82, 9-92

    conv.save_fig(fig_overlap, output_pre + ".txt", "overlap_c_unc", 12, 3, tight=True):

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir', '-d', nargs='+', help="directory for counts and ratios files")

    parser.add_argument('--output_pre', help='output_prefix')

    args = parser.parse_args()

    process_dir(args.input_dir, args.unsel, args.output_pre )
    
