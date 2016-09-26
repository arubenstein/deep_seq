#!/usr/bin/env python

"""Create edges and nodes from a list of sequences that are a given hamming distance apart"""
import itertools
import sys
import operator
import numpy as np
import argparse
from general_seq import conv
from general_seq import seq_IO
from plot import conv as pconv
import matplotlib.pyplot as plt
import math
import matplotlib


def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def plot_heatmap(ax, data, colormap, ticks, labels, xlabel, ylabel, title, vmin, vmax):
    CS = ax.pcolor(data, cmap=colormap, vmin=vmin, vmax=vmax)
    ax.set_xticklabels('')
    ax.set_yticklabels('')
    ax.set_xticks(ticks, minor=True)
    ax.set_yticks(ticks, minor=True)
    ax.set_xticklabels(labels, minor=True)
    ax.set_yticklabels(labels, minor=True)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.xaxis.set_ticks_position('none') 
    return CS

def main(sequence_file, output_prefix):
    
    sequences = seq_IO.read_sequences(sequence_file)
    n_char = len(sequences[0])

    fig, axarr = pconv.create_ax(6, 2, shx=False, shy=False)
    ticks = [ i + 0.5 for i in np.arange(0,20) ]
    aa_string = 'DEKRHNQYCGSTAMILVFWP'
    maxes = []
    mins = []

    full_data = []
    positions = []
    full_data_flat = []

    shrunk_cmap = shiftedColorMap(matplotlib.cm.bwr, start=0.25, midpoint=0.5, stop=0.75, name='shrunk')

    for ind, (pos1, pos2) in enumerate(list(itertools.combinations(range(0,5),2))):
        #print pos1, pos2, conv.covar_MI(sequences, pos1, pos2)
	data = np.zeros( (20,20) )
	for ind1, aa1 in enumerate(aa_string):
 	    for ind2, aa2 in enumerate(aa_string):
                data[ind1,ind2] = conv.calc_epi_log(sequences, pos1, pos2, aa1, aa2)
        avg_pos1 = np.sum(data, axis=1) #should check once more that this is the correct axis
        avg_pos2 = np.sum(data, axis=0)
        #I'm sure there is a cool numpy way to do this but I don't have time for it right now
        for ind1 in xrange(0, 20):
            for ind2 in xrange(0, 20):
		p = (avg_pos1[ind1]+avg_pos2[ind2]-data[ind1,ind2])/(19) #n-1=19
                #p = p if p > 0.05 else 0.05
                #data[ind1,ind2] = data[ind1,ind2]/p
	maxes.append(np.amax(data))
        mins.append(np.amin(data))
        full_data.append(data)
        positions.append((pos1, pos2))
        full_data_flat.extend(data.flatten())

    perc = np.percentile(full_data_flat, 99.9)
   
    for ind, (data, (pos1, pos2)) in enumerate(zip(full_data, positions)):
	y_ind = ind % 5
        x_ind = math.floor(ind/5)
        CS = plot_heatmap(axarr[x_ind,y_ind], data, shrunk_cmap, ticks, list(aa_string), "position {0}".format(pos2+1), "position {0}".format(pos1+1), "MI: {0:.4f}".format(conv.covar_MI(sequences, pos1, pos2)), vmin = -1.0 * perc, vmax = perc)

    average_data = np.mean(full_data, axis=0)
    max_data = np.max(full_data, axis=0)

    CS = plot_heatmap(axarr[0,5], average_data, shrunk_cmap, ticks, list(aa_string), "", "", "Averages", vmin = -1.0 * perc, vmax = perc) 

    CS = plot_heatmap(axarr[1,5], max_data, shrunk_cmap, ticks, list(aa_string), "", "", "Maximums", vmin = -1.0 * perc, vmax = perc)
    print maxes
    print mins
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
   
    plt.colorbar(CS, cax=cbar_ax)

    pconv.save_fig(fig, sequence_file, "heatmap", 18, 6, tight=False, size=7)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument ('--sequence_file', '-d', help="text file which contains sequences")

    parser.add_argument ('--output_prefix', help='output file prefix')

    args = parser.parse_args()

    main(args.sequence_file, args.output_prefix)
