#!/usr/bin/env python

"""Convenience module to perform sequence IO"""
import os

#todo - should this be a dict of additional params or something?
def read_sequences( seqfile, additional_params=False, ind_type=None):
    """Reads list of sequences. If additional_params is set to True, reads each line as a list of sequence + additional parameters in that line."""
    with open(seqfile) as f:
        lines = f.read().splitlines()
    if additional_params:
        lines = [ l.split(',') for l in lines ]
    if ind_type is not None:
        new_lines = []
        for l in lines:
            new_l = l[:]
            for ind,dtype in ind_type.items():
                new_l[ind] = dtype(l[ind])
            new_lines.append(new_l)
        lines = new_lines    
    return lines

def read_counts(counts_filename):
    """Reads counts file into dict of counts"""
    with open(counts_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = dict( (line.split()[1] , float(line.split()[8])) for line in lines if '*' not in line.split()[1] )

    return lines_proc

def read_freqs(counts_filename):
    """Reads counts file into dict of freqs"""
    with open(counts_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    lines_proc = dict( (line.split()[1] , float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )

    return lines_proc

def read_ratios(ratios_filename):
    """Reads ratios file into dict of ratios, dict of counts unselected, and dict of counts selected"""

    with open(ratios_filename) as f:
        lines = f.read().splitlines()
    lines.pop(0)
    r = dict( (line.split()[1] , float(line.split()[7])) for line in lines if '*' not in line.split()[1] )
    c_unsel = dict( (line.split()[1], float(line.split()[-2])) for line in lines if '*' not in line.split()[1] )
    c_sel = dict( (line.split()[1], float(line.split()[-1])) for line in lines if '*' not in line.split()[1] )
    return r, c_unsel, c_sel

