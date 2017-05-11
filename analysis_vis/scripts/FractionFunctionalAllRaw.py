#!/usr/bin/env python

"""Plots fraction functional variants at each step away from consensus seq."""

import itertools
import sys
import operator
import numpy
from numpy import linalg as LA
import argparse
from general_seq import seq_IO
from general_seq import conv as gsconv
import datetime

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
    print T_mat.nbytes
    return T_mat

def raise_matrix( T_matrix, power, canon_ind, orig_len ):
    raised_mat = LA.matrix_power(T_matrix,power)   
    total=numpy.count_nonzero(raised_mat[canon_ind,0:orig_len])
    mat_size=float(raised_mat[canon_ind,0:orig_len].size) 

    return total/mat_size

def square_matrix( T_matrix_new, T_mat_orig):
    raised_mat = numpy.dot(T_matrix_new,T_mat_orig)

    return raised_mat

def find_frac(T_mat, canon_ind, orig_len):
    total=numpy.count_nonzero(T_mat[canon_ind,0:orig_len])
    mat_size=float(T_mat[canon_ind,0:orig_len].size)
    return total/mat_size

def main(seq_file, canonical_file, output_prefix):

    #canonical_list_seq = seq_IO.read_sequences(canonical_file)
    canonical_list_seq = ["DEMEE","DEMED"]
    print "Beginning Script: {0}".format(datetime.datetime.now())

    with open(seq_file) as strings:
        seq_list = strings.read().splitlines()
	seq_ind_list = [ (seq, ind) for ind, seq in enumerate(seq_list) ]
    
    seq_ind_dict = { seq : ind for seq, ind in seq_ind_list }

    orig_len = len(seq_ind_list)

    edges = []
    edges_set = set()
    print "Read in Data: {0}".format(datetime.datetime.now())

    for seq, seq_ind in seq_ind_dict.items():
        neighbors = gsconv.gen_hamdist_one(seq)
        edges_set.update([ (seq, n) for n in neighbors if n in seq_ind_dict ])
        edges += [((seq, seq_ind), (n,seq_ind_dict[n])) for n in neighbors if n in seq_ind_dict and (n,seq) not in edges_set ]

    print len(seq_ind_list)
    print "Generated Edges: {0}".format(datetime.datetime.now())    

    numpy.set_printoptions(threshold='nan')

    canon_ind_dict = { canonical : [ i for (s, i) in seq_ind_list if s == canonical ][0] for canonical in canonical_list_seq }

    T_mat = trans_matrix(seq_ind_list,edges)
        #print raise_matrix(T_mat,1)
        #print raise_matrix(T_mat,3)
        #T = raise_matrix(T_mat,10)
        #T = raise_matrix(T_mat,20)
    print "Transformed Matrix: {0}".format(datetime.datetime.now())

    canon_x = { can : [0,1] for can in canonical_list_seq }
    canon_y = { can : [0.0, find_frac(T_mat, canon_ind_dict[can], orig_len)] for can in canonical_list_seq }

    print "Made x and y dicts: {0}".format(datetime.datetime.now())

    T_mat_new = T_mat

    for i in range(2,23):

	T_mat_new = square_matrix(T_mat_new, T_mat)

	for can in canonical_list_seq:
            canon_x[can].append(i)
	    canon_y[can].append(find_frac(T_mat_new, canon_ind_dict[can], orig_len))

	print "Raised Matrix {0}: {1}".format(i, datetime.datetime.now())


    series = [ [canon_x[can],canon_y[can], can] for can in canonical_list_seq ]

    with open("{0}_raw.csv".format(output_prefix),'w') as o:
        for x, y, can in series:
            o.write(can)
	    o.write("\n")
	    o.write("\n".join([ "X,{0}".format(x_val) for x_val in x ]))
            o.write("\n")
            o.write("\n".join([ "Y,{0}".format(y_val) for y_val in y ]))
            o.write("\n")
        
    print "Outputted Figure: {0}".format(datetime.datetime.now())    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', help="file of sequences to read in")

    parser.add_argument('--canonical_file', help='canonical sequence')
    parser.add_argument('--output_prefix', help='Prefix for output plot files')

    args = parser.parse_args()

    main(args.seq_file, args.canonical_file, args.output_prefix)

