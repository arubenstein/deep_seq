#!/usr/bin/env python

"""Plots fraction functional variants at each step away from consensus seq."""

import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from plot import conv
from plot import line

def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def trans_matrix( seq_list, edges ):
    T_arr = numpy.zeros(shape=(len(seq_list),len(seq_list)))
    for x,y in edges:
        x_ind = seq_list.index(x)
        y_ind = seq_list.index(y)
        T_arr[x_ind,y_ind] = 1
        T_arr[y_ind,x_ind] = 1
    totals=T_arr.sum(axis=0)
    totals_a = numpy.add(totals,1)
    #totals[totals == 0] = 1
    div = T_arr / totals_a
    T_mat = numpy.asmatrix(div)
    return T_mat

def raise_matrix( T_matrix, power, canon_ind ):
    raised_mat = LA.matrix_power(T_matrix,power)   
    total=numpy.count_nonzero(raised_mat[canon_ind])
    mat_size=float(raised_mat[canon_ind].size)
    return total/mat_size

def main(seq_file, canonical, output_prefix):

    with open(seq_file) as strings:
        seq_list = strings.read().splitlines()
    
    edges = [(seq2,seq) for seq,seq2 in itertools.combinations(seq_list,2) if hamdist(seq2,seq) < 2 ]
    
    numpy.set_printoptions(threshold='nan')

    canon_ind=seq_list.index(canonical)

    T_mat = trans_matrix(seq_list,edges)
    #print raise_matrix(T_mat,1)
    #print raise_matrix(T_mat,3)
    #T = raise_matrix(T_mat,10)
    #T = raise_matrix(T_mat,20)
    x = [0]
    y = [0]

    for i in range(1,30):
        x.append(i)
        y.append(raise_matrix(T_mat,i,canon_ind))

    fig, ax = conv.create_ax(1, 1)

    line.draw_actual_plot(x, y, "aa", ax[0,0], title="Traversing Functional Variant Graph", x_axis="# of Steps", y_axis="Fraction Variants Reached")
    ax[0,0].set_xlim(xmin=1)
    conv.save_fig(fig, output_prefix, canonical + "_fraction_func", 6, 6, size=15)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', help="file of sequences to read in")

    parser.add_argument('--canonical', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')

    args = parser.parse_args()

    main(args.seq_file, args.canonical, args.output_prefix)

