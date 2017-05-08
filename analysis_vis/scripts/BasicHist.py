#!/usr/bin/env python

"""Basic histogram script"""
import argparse
from general_seq import conv
from general_seq import seq_IO
from plot import conv as pconv
from plot import hist

def main(data_file, title, output_prefix):

    sequences = seq_IO.read_sequences(data_file, additional_params=True, header=True)

    data = [ seq_dict["Degree"] for seq, seq_dict in sequences.items() ]

    fig, axarr = pconv.create_ax(1, 1, shx=False, shy=False)

    hist.draw_actual_plot(axarr[0,0], data, "", title.capitalize(), normed=True, nbins=30, edgecolor=None, log=False)    
    #axarr[0,0].ticklabel_format(axis='x', style='sci', scilimits=(-2,2))

    pconv.save_fig(fig, output_prefix, title, 5, 5, tight=True, size=10) 

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--data_file', '-d', help="text file which contains sequences and the label you want to use for the set")

    parser.add_argument ('--title', help="title for the plot")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.data_file, args.title, args.output_prefix)
