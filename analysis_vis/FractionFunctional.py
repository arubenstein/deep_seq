#!/usr/bin/env python

"""Plots fraction functional variants at each step away from consensus seq."""

import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from plot import conv
from plot import scatterplot 
from general_seq import seq_IO
from general_seq import conv as gsconv

def trans_matrix( seq_list, edges ):
    T_arr = numpy.zeros(shape=(len(seq_list),len(seq_list)))
    for (x,x_ind),(y,y_ind) in edges:
        T_arr[x_ind,y_ind] = 1
        T_arr[y_ind,x_ind] = 1
    totals=T_arr.sum(axis=0)
    totals_a = numpy.add(totals,1)
    #totals[totals == 0] = 1
    div = T_arr / totals_a
    T_mat = numpy.asmatrix(div)
    return T_mat

def raise_matrix( T_matrix, power, canon_ind, orig_len ):
    raised_mat = LA.matrix_power(T_matrix,power)   
    total=numpy.count_nonzero(raised_mat[canon_ind,0:orig_len])
    mat_size=float(raised_mat[canon_ind,0:orig_len].size) 

    return total/mat_size

def main(seq_file, canonical_file, output_prefix):

    series = []

    canonical_list_seq = seq_IO.read_sequences(canonical_file)

    for canonical in canonical_list_seq:

        with open(seq_file) as strings:
            seq_list = strings.read().splitlines()
	    seq_ind_list = [ (seq, ind) for ind, seq in enumerate(seq_list) ]
	orig_len = len(seq_ind_list)
        if canonical not in seq_list:
	    one_away = gsconv.gen_hamdist_one(canonical)
            one_away = [ o for o in one_away if o != canonical ] + [canonical]
	    seq_ind_list = seq_ind_list[:] + [ (o, ind) for (ind, o) in enumerate(one_away, len(seq_ind_list)) ]

        edges = [(seq2,seq) for seq,seq2 in itertools.combinations(seq_ind_list,2) if gsconv.hamdist(seq2[0],seq[0]) < 2 ]
    
        numpy.set_printoptions(threshold='nan')

        canon_ind=[ i for (s, i) in seq_ind_list if s == canonical ][0]

        T_mat = trans_matrix(seq_ind_list,edges)
        #print raise_matrix(T_mat,1)
        #print raise_matrix(T_mat,3)
        #T = raise_matrix(T_mat,10)
        #T = raise_matrix(T_mat,20)
        x = [0]
        y = [0]

        for i in range(1,23):
            x.append(i)
            y.append(raise_matrix(T_mat,i,canon_ind, orig_len))

	series.append([x,y,canonical])

    fig, ax = conv.create_ax(1, 1)

    scatterplot.plot_series( ax[0,0], series, title="", x_axis="# of Steps", y_axis="Fraction Cleaved Variants Reached", alpha=1.0, connect_dots=True, size=30, edgecolors='k')
    ax[0,0].set_xlim(xmin=1)
    ax[0,0].set_ylim(ymin=0.0, ymax=1.0)
    ax[0,0].set_xticks(xrange(1,23,3))
    conv.save_fig(fig, output_prefix, "fraction_func", 6, 6, size=15)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', help="file of sequences to read in")

    parser.add_argument('--canonical_file', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')

    args = parser.parse_args()

    main(args.seq_file, args.canonical_file, args.output_prefix)

