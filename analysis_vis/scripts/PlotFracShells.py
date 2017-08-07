#!/usr/bin/env python

"""bar plot to plot fraction shell cleaved"""
from plot import conv as pconv
from plot import bar
from general_seq import seq_IO
import argparse
import numpy as np 

def main(sequence_ratio_file, width, height, pattern, legend):

    sequences = seq_IO.read_sequences(sequence_ratio_file, additional_params=True)

    shell_data = []

    for shell in xrange(1,len(sequences[0])):
        shell_data.append([ seq[shell] for seq in sequences ])

    avg = []
    std = []
    label = xrange(1,4)

    for sd in shell_data:
        avg.append( np.median(sd))
        std.append( np.std(sd))

    #check if std has to be fixed
    #if sum([ 1 for a, s in zip(avg_ratio, std) if a - s < 0 ]):
    #    min_err = [ a - s if a - s >= 0.0 else 0 for a,s in zip(avg_ratio, std) ]
    #    max_err = [ a + s for a,s in zip(avg_ratio, std) ]
    #    err = [min_err, max_err]
    #else:
    #    err = std

    err = std

    fig, axarr = pconv.create_ax(1, 1, shx=True, shy=True)

    bar.draw_actual_plot(axarr[0,0], avg, ['lightsteelblue','lightblue','darkgray'], "", "Shell", "Fraction Cleaved", tick_label=label, yerr = err)
    #axarr[0,0].set_ylim([0,1.3])
    pconv.save_fig(fig, sequence_ratio_file, "plot", width, height, tight=True, size=10)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_ratio_file', help="Text file that contains name of sequences, avg ratio, std. and label.")

    parser.add_argument ('--width')
    parser.add_argument ('--height')
    parser.add_argument ('--pattern', action='store_true', default=False)
    parser.add_argument ('--legend', action='store_true', default=False)
    args = parser.parse_args()

    main(args.sequence_ratio_file, args.width, args.height, args.pattern, args.legend)
