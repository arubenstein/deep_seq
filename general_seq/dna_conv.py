#!/usr/bin/env python

'''specialized DNA convenience tools'''

import collections
from string import ascii_uppercase
import math
import itertools

gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

rev = collections.defaultdict(list)
for k, v in gencode.items():
    rev[v].append(k)

ambig_codes = {
    'Y':['C','T'],
    'R':['A','G'],
    'W':['T','A'],
    'S':['C','G'],
    'K':['G','T'],
    'M':['C','A'],
    'D':['A','T','G'],
    'V':['C','A','G'],
    'H':['C','T','A'],
    'B':['C','T','G'],
    'X':['C','T','A','G'],
    'N':['C','T','A','G']}


#kept this even though it's identical to the general one because I don't want to import that module here and then have issues with function names
def hamdist(str1, str2):
    '''Determines hamming distance between two strings'''
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def gen_hamdist_one(seq):
    aa_string = 'CTAG'

    return [ seq[0:ind] + char + seq[ind+1:] for ind in xrange(0,len(seq)) for char in aa_string if char != seq[ind] ] 

def translate(dna_string):
    list_aa_ambig = [gencode.get(dna_string[3*i:3+3*i], dna_string[3*i:3+3*i]) for i in xrange(len(dna_string)//3) ]
    list_aa_res = []
    alphabets = []
    for aa in list_aa_ambig:
        if len(aa) == 1:
            list_aa_res.append(aa)
        else:
            alphabets = [ ambig_codes.get(dna,[dna]) for dna in aa ]
	    codons = [''.join(a) for a in itertools.product(*alphabets) ]
            trans = set([ gencode[c] for c in codons ])
            if len(trans) > 1:
                list_aa_res.append('X')
            else:
                list_aa_res.append(list(trans)[0])
    
    return ''.join(list_aa_res)

def rev_translate(aa_string):
    alphabets = [ rev[aa] for aa in aa_string ]
    trans = [ "".join(a) for a in itertools.product(*alphabets) ]
    return trans 

def find_next_node(path, target, new_paths): 
    source = path[-1]
    if source == target:
	
        return path
    else:
        next_nodes = [ source[0:ind] + char + source[ind+1:] for ind,char in enumerate(target) if char != source[ind] ]
	paths = [ path + [n] for n in next_nodes ]
	for p in paths:
	     next_paths = find_next_node(p, target, new_paths)
             if next_paths:
	         new_paths.append(next_paths)

def frac_paths(source, target, cleaved_set):
    paths = []
    find_next_node([source], target, paths) 

    unpassable = sum([1 for path in paths if any(p not in cleaved_set for p in path[1:-1]) ])

    return float(unpassable)/len(paths)

def adj_list(cleaved_set, uncleaved_set, middle_set, list_from, ignore_middle=False):
    neighbors = {} 
    for seq in list_from:
        neighbors_set = set(gen_hamdist_one(seq))
        cl_neighbors = neighbors_set.intersection(cleaved_set)
        uncl_neighbors = neighbors_set.intersection(uncleaved_set)
	if not ignore_middle:
            mid_neighbors = neighbors_set.intersection(middle_set)
        neighbors[seq] = {}
        neighbors[seq]["CLEAVED"] = cl_neighbors
        neighbors[seq]["UNCLEAVED"] = uncl_neighbors
        if not ignore_middle: 
            neighbors[seq]["MIDDLE"] = mid_neighbors
    	else:
	    neighbors[seq]["MIDDLE"] = []
    return neighbors 

def adj_list_cleaved(cleaved_set, list_from):
    neighbors = {}
    for seq in list_from:
        neighbors_set = set(gen_hamdist_one(seq))
        cl_neighbors = neighbors_set.intersection(cleaved_set)
        neighbors[seq] = {}
        neighbors[seq]["CLEAVED"] = cl_neighbors
    return neighbors
