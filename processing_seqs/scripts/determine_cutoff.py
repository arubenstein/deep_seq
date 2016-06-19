#!/usr/bin/env python

from scipy.stats.stats import pearsonr
import glob
import os
import sys
import argparse
from plot import conv
from plot import scatterplot
import numpy as np

def read_files(counts_filename, ratios_filename):
    if counts_filename is not None:
        c = read_counts(counts_filename)
        r, blank = read_ratios(ratios_filename)
    else:
        r, c = read_ratios(ratios_filename, inc_counts=True)
    return c, r

def read_counts(counts_filename):
    with open(counts_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = dict( (line.split()[1] , float(line.split()[8])) for line in lines if '*' not in line.split()[1] )

    return lines_proc

def read_ratios(ratios_filename, inc_counts=False):
    with open(ratios_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    r = dict( (line.split()[1] , float(line.split()[7])) for line in lines if '*' not in line.split()[1] )
    if inc_counts:
        c_unsel = dict( (line.split()[1], float(line.split()[-1])) for line in lines if '*' not in line.split()[1] )
    else:
        c_unsel = None
    return r, c_unsel

def combine_counts_ratios(counts, ratios, low_cutoff, high_cutoff, st=""):
    merged = dict( (key , (counts[key],ratios[key])) for key in counts if key in ratios and counts[key] >= low_cutoff and counts[key] <= high_cutoff )
    #merged = { key : (counts[key],ratios[key]) for key in counts if key in ratios }
    if st == "":
        new_merged = [ (c,r) for key, (c,r) in merged.items() ]
    elif st == "median" or st == "mean":
        dict_mean = {}
        new_merged = []

        for key, (counts, ratios) in merged.items():
            if dict_mean.get(counts) is None:
                dict_mean[counts] = []
            dict_mean[counts].append(ratios)

        if st == "mean":
            for counts, list_ratios in dict_mean.items():
                new_merged.append( (counts, np.mean(list_ratios) ))
    	else:
            for counts, list_ratios in dict_mean.items():
                new_merged.append( (counts, np.median(list_ratios) ))
    else:
	raise ValueError()

    return new_merged

def find_coeff_pval(merged, ax, title):

    c_list = [ c for c,r in merged ]
    r_list = [ r for c,r in merged ]

    scatterplot.draw_actual_plot(ax, c_list, r_list, 'k', title, "Counts", "Ratios")
    #scatterplot.plot_regression(ax, c_list, r_list, fit=True, neg=True)
    #scatterplot.add_x_y_line(ax, neg=True)

    coeff, pval = pearsonr(c_list, r_list)
    conv.add_text_dict(ax, { "PCC" : coeff, "p-val" : pval })
    return coeff, pval

def plot_coeff_pval(ax, counters, coeffs, pvals, title=""):
    scatterplot.draw_actual_plot(ax, counters, coeffs, 'b', title, "Counts", "PCC")
    blank,sec_ax = scatterplot.draw_actual_plot(ax, counters, pvals, 'r', title, "Counts", "Pvals", secondary_y=True)
    conv.add_hor_line(sec_ax, y=0.05, color='r')
    cutoff = [ counter for pval, counter in zip(pvals, counters) if pval > 0.05 ]
    if len(cutoff) > 0:
        conv.add_ver_line(ax, x=cutoff[0], color='r')

    conv.add_hor_line(ax, y=-0.1, color='b')
    cutoff = [ counter for coeff, counter in zip(coeffs, counters) if coeff > -0.1 ]
    if len(cutoff) > 0:
        conv.add_ver_line(ax, x=cutoff[0], color='b')

def gen_plots(c, r, ax2, output_pre, dirname, st=""):
    fig, axarr = conv.create_ax(1, 31, shx=True, shy=True)

    counters = []
    coeffs = []
    pvals = []
    for i in xrange(1,31):
        m = combine_counts_ratios(c, r, i, i+9, st=st)
        coeff, pval = find_coeff_pval(m, axarr[i-1,0], "Sliding Window: {0} to {1}".format(i, i+9) )
        print i, coeff, pval
        counters.append(i)
        coeffs.append(coeff)
        pvals.append(pval)

    plot_coeff_pval(axarr[30,0], counters, coeffs, pvals)
    suffix = os.path.normpath(dirname).split(os.sep)[-3]
    conv.save_fig(fig, output_pre + "correlation_plot.txt", "{0}_{1}".format(suffix,st), 4, 20*4)

    plot_coeff_pval(ax2, counters, coeffs, pvals, suffix)

def process_dir(dirnames, unsel, output_pre):
    fig_all, axarr_all = conv.create_ax(len(dirnames), 3, shx=True, shy=True)
    for ind,dirname in enumerate(dirnames):
        print dirname
        counts_fn = dirname + '/counts_' + unsel + '*_PRO_qc'
        ratios_fn = dirname + '/ratios_*_PRO_qc'

        c_fn = glob.glob(counts_fn)
        if len(c_fn) == 0:
            c_fn = None
        else:
            c_fn = c_fn[0]
        r_fn = glob.glob(ratios_fn)[0]
        
        c,r = read_files(c_fn, r_fn)
        
        gen_plots(c, r, axarr_all[0,ind], output_pre, dirname, st="")
        gen_plots(c, r, axarr_all[1,ind], output_pre, dirname, st="mean")
        gen_plots(c, r, axarr_all[2,ind], output_pre, dirname, st="median")

    conv.save_fig(fig_all, output_pre + "all_coeff_pval.txt", "", 4*len(dirnames), 12)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--input_dir', '-d', nargs='+', help="directory for counts and ratios files")

    parser.add_argument('--unsel', help='name of unsel i.e. Sample2')

    parser.add_argument('--output_pre', help='output_prefix')

    args = parser.parse_args()

    process_dir(args.input_dir, args.unsel, args.output_pre )
    
