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
from plot import conv as pconv
from plot import scatterplot 
from plot import bar
from matplotlib_venn import venn2

def plot_epi(epistasis, total, ax, title_pre):
    bar.draw_actual_plot(ax, [ e/total for e, total in zip(epistasis, total) ], 'g', title_pre + " Epistasis", "# of Mutations", "Fraction of Total Cases", tick_label=xrange(2,6) )

def main(epistasis_file):
    
    dict_epistasis = {} #list of list of sequences, where each item represents a label 

    with open(epistasis_file) as e:
        lines = e.readlines()
        for l in lines[1:]: #ignore header line
	    tokens = l.split(',')
	    #value consists of Starting Fitness, Ending_Fitness,Epistasis,List_Seqs_Fitnesses_Intermediates 
	    if dict_epistasis.get((tokens[2], tokens[0])) is None:
                dict_epistasis[tokens[0]] = [ tokens[1], tokens[2], float(tokens[3]), tokens[4::2], [ t.strip() for t in tokens[5::2] ] ]


    '''
    n_functional = [0] * 4
    n_should_be_functional = [0] * 4
    n_total = [0] * 4

    for i in xrange(2,6):
	ind = i-2
        neg_epistasis[ind] = sum([ 1 for key, value in dict_epistasis.items() if value[2] < -0.000005 and value[4] == i ])
        no_epistasis[ind] = sum([ 1 for key, value in dict_epistasis.items() if abs(value[2]) < 0.000005 and value[4] == i ])
        pos_epistasis[ind] = sum([ 1 for key, value in dict_epistasis.items() if value[2] > 0.000005 and value[4] == i ])
	n_functional[ind] = sum([ 1 for key, value in dict_epistasis.items() if value[3] == "CLEAVED" and value[4] == i ])
        n_should_be_functional[ind] = sum([ 1 for key, value in dict_epistasis.items() if all(v == "CLEAVED" for v in value[6]) and value[4] == i ])
	n_total[ind] = float(sum([ 1 for key, value in dict_epistasis.items() if value[4] == i]))
    '''

    seq_func = set([ key for key,val in dict_epistasis.items() if val[1] == "CLEAVED" ])
    seq_pred_func = set([ key for key,val in dict_epistasis.items() if all(v == "CLEAVED" for v in val[4]) ]) 

    seq_unfunc = set([ key for key,val in dict_epistasis.items() if val[1] == "UNCLEAVED" ])
    seq_pred_unfunc = set([ key for key,val in dict_epistasis.items() if any(v == "UNCLEAVED" for v in val[4]) or sum(v == "MIDDLE" for v in val[4]) == 2 ])

    seq_midfunc = set([ key for key,val in dict_epistasis.items() if val[1] == "MIDDLE" ])
    seq_pred_midfunc = set([ key for key,val in dict_epistasis.items() if any(v == "MIDDLE" for v in val[4]) ])   
 
    #fig, axarr = pconv.create_ax(3, 1, shx=True, shy=True)
    #fig2, axarr2 = pconv.create_ax(1, 1)
    #plot_epi(neg_epistasis, n_total, axarr[0,0], "Negative")
    #plot_epi(no_epistasis, n_total, axarr[0,1], "No")
    #plot_epi(pos_epistasis, n_total, axarr[0,2], "Positive")
    #n_func_frac = [ func/total for func, total in zip(n_functional, n_total) ]
    #n_pred_frac = [ pred/total for pred, total in zip(n_should_be_functional, n_total) ]
    #scatterplot.plot_series(axarr2[0,0], [(range(2,6),n_func_frac,"% Cleaved"),(range(2,6),n_pred_frac,"% Pred Cleaved")], "", "Number of Mutations", "Fraction of Total Cases", size=40, connect_dots=True, alpha=1.0)
    #axarr2[0,0].set_ylim([0,1.0])
    fig_venn, axarr_venn = pconv.create_ax(1, 1)
    fig_vennun, axarr_vennun = pconv.create_ax(1, 1)
    fig_vennmid, axarr_vennmid = pconv.create_ax(1, 1)

    venn2([seq_func, seq_pred_func], set_labels = ["Cleaved", "Pred Cleaved"], ax=axarr_venn[0,0])
    venn2([seq_unfunc, seq_pred_unfunc], set_labels = ["Uncleaved", "Pred Uncleaved"], ax=axarr_vennun[0,0])
    venn2([seq_midfunc, seq_pred_midfunc], set_labels = ["Middle", "Pred Middle"], ax=axarr_vennmid[0,0])

    #pconv.save_fig(fig, epistasis_file, "plot", 12, 4, tight=True, size=12)
    #pconv.save_fig(fig2, epistasis_file, "pred_v_cl", 5, 5, tight=True, size=10)
    pconv.save_fig(fig_venn, epistasis_file, "venn", 5, 5, tight=False, size=14)
    pconv.save_fig(fig_vennun, epistasis_file, "vennun", 5, 5, tight=False, size=14)
    pconv.save_fig(fig_vennmid, epistasis_file, "vennmid", 5, 5, tight=False, size=14)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--epistasis_file', help="text file which contains epistasis data (as generated by EpistasisAllSeqs)")

    args = parser.parse_args()

    main(args.epistasis_file)
