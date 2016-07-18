#!/usr/bin/env python

import os
import sys
import argparse
from plot import conv
from plot import scatterplot
import numpy as np

def read_ratios(ratios_filename):
    with open(ratios_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    r = dict( (line.split()[1] , float(line.split()[7])) for line in lines if '*' not in line.split()[1] )
    c_unsel = dict( (line.split()[1], float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )
    c_sel = dict( (line.split()[1], float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )
    return r, c_unsel, c_sel

def plot_corr(c_1, c_2, ax, x_axis, y_axis):
    scatterplot.draw_actual_plot(ax, c_1, c_2, 'b', "Counts vs. Counts", x_axis, y_axis, size=10)

    scatterplot.plot_regression(ax, c_1, c_2)

def common_points(counts1, counts2, filtered=False):
    c_1 = []
    c_2 = []

    mu=np.mean(counts1.values()+counts2.values())
    sigma=np.std(counts1.values()+counts2.values())
    
    for k,val in counts1.items():
        if counts2.get(k) is not None:
            if not filtered or ( (val-mu)/sigma < 25 and (counts2[k]-mu)/sigma < 25 ):
                c_1.append(val)
                c_2.append(counts2[k])
    return c_1, c_2

def main(ratios_file1, ratios_file2, output_pre, use_sel):
   if use_sel:
       counts1_dict = read_ratios(ratios_file1)[2]
       counts2_dict = read_ratios(ratios_file2)[2]
       title1 = os.path.basename(ratios_file1).split("_")[1]
       title2 = os.path.basename(ratios_file2).split("_")[1]
   else:
       counts1_dict = read_ratios(ratios_file1)[1]
       counts2_dict = read_ratios(ratios_file2)[1]
       title1 = os.path.basename(ratios_file1).split("_")[6]
       title2 = os.path.basename(ratios_file2).split("_")[6]
   fig, axarr = conv.create_ax(2, 1)

   c1, c2 = common_points(counts1_dict, counts2_dict)
   plot_corr(c1, c2, axarr[0,0], title1, title2)
   c1, c2 = common_points(counts1_dict, counts2_dict, filtered=True)
   plot_corr(c1, c2, axarr[0,1], title1, title2)


   conv.save_fig(fig, output_pre + "/corrcounts.txt", title1 + "_" + title2, 20, 10, tight=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--ratios_file1', help='name of first ratios file with path')
    parser.add_argument('--ratios_file2', help='name of second ratios file with path')

    parser.add_argument('--output_pre', help='output_prefix')

    parser.add_argument('--use_sel', dest='use_sel', action='store_true')
    parser.add_argument('--use_unsel', dest='use_sel', action='store_false')
    args = parser.parse_args()

    main(args.ratios_file1, args.ratios_file2, args.output_pre, args.use_sel) 
