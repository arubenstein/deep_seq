#!/usr/bin/env python

"""Basic bar plot used for validation of sequences"""
from plot import conv as pconv
from plot import bar
from general_seq import seq_IO
import argparse 

def convert_label_color(label):
    if label == "CLEAVED":
	color = 'lightskyblue'
    elif label == "UNCLEAVED":
        color = 'tomato'
    else:
        color = 'black'
    return color

def main(sequence_ratio_file, width, height, pattern, legend):

    sequence_ratio = seq_IO.read_sequences(sequence_ratio_file, additional_params=True)

    seqs = [ s[0] for s in sequence_ratio ]
    avg_ratio = [ s[1] for s in sequence_ratio ]
    std = [ s[2] for s in sequence_ratio ]
    label = [ s[3] for s in sequence_ratio ]

    if len(sequence_ratio[0]) > 4:
        color = [ s[4] for s in sequence_ratio ]
    else:
        color = [ convert_label_color(l) for l in label ]

    #check if std has to be fixed
    #if sum([ 1 for a, s in zip(avg_ratio, std) if a - s < 0 ]):
    #    min_err = [ a - s if a - s >= 0.0 else 0 for a,s in zip(avg_ratio, std) ]
    #    max_err = [ a + s for a,s in zip(avg_ratio, std) ]
    #    err = [min_err, max_err]
    #else:
    #    err = std

    err = std

    fig, axarr = pconv.create_ax(1, 1, shx=True, shy=True)

    if legend:
	label_legend = [ l if l not in ["CLEAVED","MIDDLE","UNCLEAVED"] else None for l in label ]
        patches, labels = bar.draw_actual_plot(axarr[0,0], avg_ratio, color, "", "", "FLAG/HA Ratio", tick_label=seqs, yerr = err, pattern=pattern, label=label_legend)
        lgd = axarr[0,0].legend(patches,labels, loc="upper center", bbox_to_anchor=(0.5,1.05), borderaxespad=0., prop={'size':9}, ncol=2, fancybox=True)
        print patches
        print labels
    else:
        bar.draw_actual_plot(axarr[0,0], avg_ratio, color, "", "", "FLAG/HA Ratio", tick_label=seqs, yerr = err, pattern=pattern)
	lgd = None 
    axarr[0,0].set_ylim([0,1.3])
    pconv.save_fig(fig, sequence_ratio_file, "plot", width, height, tight=True, size=10, extra_artists=lgd)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_ratio_file', help="Text file that contains name of sequences, avg ratio, std. and label.")

    parser.add_argument ('--width')
    parser.add_argument ('--height')
    parser.add_argument ('--pattern', action='store_true', default=False)
    parser.add_argument ('--legend', action='store_true', default=False)
    args = parser.parse_args()

    main(args.sequence_ratio_file, args.width, args.height, args.pattern, args.legend)
