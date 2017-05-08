#!/usr/bin/env python

"""Basic histogram script"""
import argparse
from general_seq import conv
from general_seq import seq_IO
from plot import conv as pconv
from plot import hist
from plot import bar
import numpy as np
from collections import defaultdict

def main(data_file, output_prefix, degree_file, width, height):

    sequences = seq_IO.read_sequences(data_file, additional_params=True, header=True, list_vals=True)
    seq_degree = seq_IO.read_sequences(degree_file, additional_params=True, header=True)

    degree_frac = defaultdict(list)

    for seq, seq_dict in sequences.items():
        degree_frac[seq_degree[seq]['Degree']].append(np.mean(seq_dict["Frac"]))

    data = [ np.mean(seq_dict["Frac"]) for seq, seq_dict in sequences.items() ]

    degree_frac_avg = [ np.mean(list_fracs) for degree, list_fracs in degree_frac.items() ]
    degree_frac_std = [ np.std(list_fracs) for degree, list_fracs in degree_frac.items() ]

    fig, axarr = pconv.create_ax(1, 1, shx=False, shy=False)

    hist.draw_actual_plot(axarr[0,0], data, "", "", normed=False, nbins=30, edgecolor=None, log=False)    
    #axarr[0,0].ticklabel_format(axis='x', style='sci', scilimits=(-2,2))

    pconv.save_fig(fig, output_prefix, "hist", width, height, tight=True, size=10) 

    fig2, axarr2 = pconv.create_ax(1, 1, shx=True, shy=True)

    bar.draw_actual_plot(axarr2[0,0], degree_frac_avg, 'g', "", "Degree", "Fraction Shortest Path Uncleaved", tick_label=degree_frac.keys(), yerr=degree_frac_std)
    #axarr[0,0].set_ylim([0,1.3])
    pconv.save_fig(fig2, output_prefix, "bar", width, height, tight=True, size=10)
 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--data_file', '-d', help="text file which contains sequences and frac uncleaved")

    parser.add_argument ('--degree_file', help="text file which contains sequences and degrees")

    parser.add_argument ('--output_prefix', help='output file prefix')

    parser.add_argument ('--width')
    parser.add_argument ('--height') 

    args = parser.parse_args()

    main(args.data_file, args.output_prefix, args.degree_file, args.width, args.height)
