#!/usr/bin/env python

from scipy.stats.stats import pearsonr
import glob
import os
import sys
import argparse
from plot import conv
from plot import scatterplot
import numpy as np
from plot import line
from shapely.geometry import LineString
from shapely.geometry import Point

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
    freq_ratios_all = [ abs(freq1-freq_dict2[key])/freq1 for key, freq1 in freq_dict1.items() if key in freq_dict2 ]
    freq_ratio_perc = np.percentile(freq_ratios_all, 75)
    return freq_ratio_perc

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def normalize_list(list_vals, normtype="all"):
    max_val = float(max(list_vals))
    min_val = float(min(list_vals))
    diff = float(max_val-min_val)
    print normtype
    if normtype == "all":
        normed = [ (v-min_val)/diff for v in list_vals ]
    elif normtype == "top":
        normed = [ v/diff for v in list_vals ]
    else:
        raise ValueError
    return normed

def plot_curve(ax, x, y, label, title, x_axis, y_axis, norm=None):
    print norm
    if norm is not None:
        print "about to normalize"
        norm_x = normalize_list(x, normtype=norm)
        norm_y = normalize_list(y)
    else:
        print "not normalizing x"
        norm_x = x
        norm_y = normalize_list(y)
    
    scatterplot.plot_series(ax, [[norm_x, norm_y, label]], title, x_axis, y_axis, connect_dots=True)
    #ax.plot([0, 0.5], [1, 0.5], c='b')
    #line1 = LineString(zip(x,y))
    #line2 = LineString([(0,1),(1,0)])

    #min_distance_point = (sorted([ (Point(x_val,y_val).distance(line2), ind, x_val, y_val) for ind, (x_val, y_val) in enumerate(zip(x,y),1)]))[0]

    #point = line1.intersection(line2)

    #conv.annotate_point(ax, min_distance_point[2], min_distance_point[3], "({0:.2f},{1:.2f}) at: {2}".format(min_distance_point[2], min_distance_point[3], min_distance_point[1]))
    x_cutoff = 0.10 if norm is not None else 0.25
    conv.add_ver_line(ax, ymin=0, ymax=1, x=x_cutoff, color='k')
    line2 = LineString([(x_cutoff,0),(x_cutoff,1)])

    min_distance_point = (sorted([ (Point(x_val,y_val).distance(line2), ind, x_val, y_val) for ind, (x_val, y_val) in enumerate(zip(norm_x,norm_y),1)]))[0]

    conv.annotate_point(ax, min_distance_point[2], min_distance_point[3], "({0:.2f},{1:.2f}) at: {2}".format(min_distance_point[2], min_distance_point[3], min_distance_point[1]))

    #dx = np.diff(norm_x)
    #threshold = -1
    #for i in xrange(0,len(dx)-3):
    #    if all( abs(dx[ind]) < 0.01 for ind in xrange(i, i+3)):
    #        x_val = x[i]
    #        y_val = y[i]
    #        threshold = i
    #        break
    #if threshold > -1:
    #    conv.annotate_point(ax, x_val, y_val, "({0:.2f},{1:.2f}) at: {2}".format(x_val, y_val, threshold))

def process_dir(initial_dir, output_pre):

    #almost no error-catching - assumes that all directories from 0-30 are present

    #set up lists
    samplesize = { "MP011Tr20_Fr1_MP012Tr20_Fr1" : [], 
                   "MP021Tr20_Fr1_MP022Tr20_Fr1" : [],
                   "MP091Tr20_Fr1_MP092Tr20_Fr1" : [],
                   "MP101Tr20_Fr1_MP102Tr20_Fr1" : [], 
                   "MP02Tr20_Fr3_MP07Tr20_Fr3" : [],
                   "MP02Tr20_Fr3_MP08Tr20_Fr3" : [],
                   "MP02Tr20_Fr3_MP09Tr20_Fr3" : [] }

    overlap_c_unc = { "MP011Tr20_Fr1_MP012Tr20_Fr1_MP011Tr20_Fr1_MP013Tr20_Fr1": ( [], "MP011Tr20_Fr1_MP012Tr20_Fr1"),
                      "MP021Tr20_Fr1_MP022Tr20_Fr1_MP021Tr20_Fr1_MP023Tr20_Fr1": ( [], "MP021Tr20_Fr1_MP022Tr20_Fr1"),
                      "MP091Tr20_Fr1_MP092Tr20_Fr1_MP091Tr20_Fr1_MP093Tr20_Fr1": ( [], "MP091Tr20_Fr1_MP092Tr20_Fr1"),
                      "MP101Tr20_Fr1_MP102Tr20_Fr1_MP101Tr20_Fr1_MP103Tr20_Fr1": ( [], "MP101Tr20_Fr1_MP102Tr20_Fr1"),
                      "MP02Tr20_Fr3_MP07Tr20_Fr3_MP02Tr20_Fr3_MP09Tr20_Fr3": ( [], "MP02Tr20_Fr3_MP07Tr20_Fr3") }

    freq_freq = { ("MP02Tr20_Fr3_MP07Tr20_Fr3","MP02Tr20_Fr3_MP72Tr20_Fr3") : ( [], "MP02Tr20_Fr3_MP07Tr20_Fr3"),
                  ("MP02Tr20_Fr3_MP08Tr20_Fr3","MP02Tr20_Fr3_MP82Tr20_Fr3") : ( [], "MP02Tr20_Fr3_MP08Tr20_Fr3"),
                  ("MP02Tr20_Fr3_MP09Tr20_Fr3","MP02Tr20_Fr3_MP92Tr20_Fr3") : ( [], "MP02Tr20_Fr3_MP09Tr20_Fr3") }

    ratios = { "MP07Tr20_Fr3_MP72Tr20_Fr3" : ( [], "MP02Tr20_Fr3_MP07Tr20_Fr3"),
               "MP08Tr20_Fr3_MP82Tr20_Fr3" : ( [], "MP02Tr20_Fr3_MP08Tr20_Fr3"),
               "MP09Tr20_Fr3_MP92Tr20_Fr3" : ( [], "MP02Tr20_Fr3_MP09Tr20_Fr3") }


    #for each dirname, glob find all the directories within this dirname
    for threshold in xrange(1,20):
        path_prefix = os.path.join(initial_dir,str(threshold))
        #todo: check that it exists

        for key in samplesize.keys():
            print key
            print os.path.join(path_prefix, key, "data", "output", "avg_ratios_*DNA_qc")
            ratios_fname = glob.glob(os.path.join(path_prefix, key, "data", "output", "avg_ratios_*DNA_qc"))[0]
            uniq_seq = file_len(ratios_fname)
            ratios_fname = glob.glob(os.path.join(initial_dir, "1", key, "data", "output", "avg_ratios_*DNA_qc"))[0]
            tot_uniq_seq = file_len(ratios_fname)            

            samplesize[key].append(uniq_seq/float(tot_uniq_seq))
         
        #do the following for 3 pairs of 7-72 and so on
        for freq1, freq2 in freq_freq.keys():
           freq1_filename = "counts_" + '_'.join(freq1.split("_")[2:]) + ".fast_R1_DNA_qc"
           freq2_filename = "counts_" + '_'.join(freq2.split("_")[2:]) + ".fast_R1_DNA_qc"
           fr = calc_freq_ratio(os.path.join(path_prefix, freq1, "data", "output", freq1_filename), os.path.join(path_prefix, freq2, "data", "output", freq2_filename))
           freq_freq[(freq1,freq2)][0].append(fr)

        #collect the ratios for 7-72 - take their abs values and then find the 75th percentile
        for r_name in ratios.keys():
            ratios_fname = glob.glob(os.path.join(path_prefix, r_name, "data", "output", "avg_ratios_*DNA_qc"))[0]
            r, c_unsel, c_sel = read_ratios(ratios_fname)
            r_perc = np.percentile([abs(r_val) for key,r_val in r.items()], 75)
            ratios[r_name][0].append(r_perc)
        
        #find the cleaved_uncleaved overlap.txt file for each of hardcoded cleaved/uncleaved filenames
        for o in overlap_c_unc.keys():
            overlap_c_unc[o][0].append(file_len(os.path.join(path_prefix,o+"_overlap.txt")))

    #plot all figures
    #1. Overlap between cleaved and uncleaved.  Four subplots, one for each set of cleaved/uncleaved

    plot_dict(overlap_c_unc, samplesize, output_pre, "overlap_c_unc", "Overlap Between Cleaved and Uncleaved", norm="all")
    #plot_dict(freq_freq, samplesize, output_pre, "freq_freq", "abs(Freq-Freq)/Freq")
    #plot_dict(ratios, samplesize, output_pre, "ratios", "Enrich Ratio", norm="top")
    #plot_dict(ratios, samplesize, output_pre, "ratios", "Enrich Ratio", norm=None)
    plot_dict(ratios, samplesize, output_pre, "ratios", "Enrich Ratio", norm="all")

    for key, val in overlap_c_unc.items():
        print key
        for ind, item in enumerate(normalize_list(val[0]), 1):
            print "{0}\t{1}".format(ind, item)

    #2. abs(freq7-freq72)/freq7. Three subplots, one for each set of 7-72, 8-82, 9-92

    #3. abs(ratio(7,72)). Three subplots, one for each set of 7-72, 8-82, 9-92
    

def plot_dict(dict_to_plot, samplesize, output_pre, suffix, x_axis, norm="all"):
    fig, axarr = conv.create_ax(len(dict_to_plot), 1, shx=True, shy=True)

    for ind, (key, (val,sample_name)) in enumerate(dict_to_plot.items()):
        samplesize_list = [ l for k, l in samplesize.items() if k == sample_name ][0] #assume only one item meets that criteria
        title = ''.join(key)[0:28]
        plot_curve(axarr[0,ind], val, samplesize_list, "", title, x_axis, "Sample Size", norm=norm)
    conv.save_fig(fig, output_pre + (norm if norm is not None else "none"), suffix, len(dict_to_plot)*4, 4, tight=True, size=10)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir', '-d', help="directory for counts and ratios files")

    parser.add_argument('--output_pre', help='output_prefix')

    args = parser.parse_args()

    process_dir(args.input_dir, args.output_pre )
    
