#!/usr/bin/env python

import collections
from string import ascii_uppercase
import math
import itertools

def hamdist(str1, str2):
    '''Determines hamming distance between two strings'''
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def gen_hamdist_one(seq):
    aa_string = 'DEKRHNQYCGSTAMILVFWP'

    return [ seq[0:ind] + char + seq[ind+1:] for ind in xrange(0,len(seq)) for char in aa_string if char != seq[ind] ] 
 

def covar_MI(list_seqs, pos1, pos2):
    e1 = calc_entropy(calc_probs(retrieve_freq_one_pos(list_seqs, pos1)))
    e2 = calc_entropy(calc_probs(retrieve_freq_one_pos(list_seqs, pos2)))
    e_both = calc_entropy(calc_probs(retrieve_freq_two_pos(list_seqs, pos1, pos2)))
    return e1 + e2 - e_both 

def retrieve_freq_one_pos(list_seqs, pos):
    list_str = ''.join([ s[pos] for s in list_seqs ])
    dict_letters = {}
    for letter in ascii_uppercase:
        dict_letters[letter] = list_str.count(letter)
    lambda_term = len(list_seqs)/20.0 #as seen in Buslje et al. 2009
    corrected_dict = { key : lambda_term + value for key, value in dict_letters.items() }
    return corrected_dict

def retrieve_freq_two_pos(list_seqs, pos1, pos2):
    list_str = [ s[pos1] + s[pos2] for s in list_seqs ]
    dict_letters = collections.defaultdict(int)
    for item in list_str:
        dict_letters[item] += 1
    lambda_term = len(list_seqs)/400.0 #as seen in Buslje et al. 2009
    corrected_dict = { key : lambda_term + value for key, value in dict_letters.items() }
    return corrected_dict

def calc_probs(dict_letters):
    total = float(sum(dict_letters.values()))
    new_dict = { key : val/total for key, val in dict_letters.items() }
    return new_dict

def calc_entropy(dict_probs_letters):
    terms = [ p * math.log(p, 20) for p in dict_probs_letters.values() if p != 0]
    return -1.0 * sum(terms)

def calc_epi_log(list_seqs, pos1, pos2, aa1, aa2):
    f1 = retrieve_freq_one_pos(list_seqs, pos1).get(aa1,0)
    f2 = retrieve_freq_one_pos(list_seqs, pos2).get(aa2,0)
    f_both = retrieve_freq_two_pos(list_seqs, pos1, pos2).get(aa1+aa2,0)

    p1 = calc_probs(retrieve_freq_one_pos(list_seqs, pos1)).get(aa1,0)
    p2 = calc_probs(retrieve_freq_one_pos(list_seqs, pos2)).get(aa2,0)
    p_both = calc_probs(retrieve_freq_two_pos(list_seqs, pos1, pos2)).get(aa1+aa2,0)
    if p_both == 0 or p1 + p2 == 0:
        return 0
    epi = math.log((p_both/(p1*p2)), 20)
    return epi 

def fraction_neighbors_cleaved(cleaved_list, uncleaved_list, middle_list, list_from, test_existence=False):
    list_floats = {}

    for seq in list_from:
	if test_existence and seq not in cleaved_list:
	    continue
        cleaved_seqs = sum([1 for s in cleaved_list if hamdist(seq,s) == 1])
        uncleaved_seqs = sum([1 for s in uncleaved_list if hamdist(seq,s) == 1])
        middle_seqs = sum([1 for s in middle_list if hamdist(seq,s) == 1])
        if cleaved_seqs > 0 or uncleaved_seqs > 0 or middle_seqs > 0:
            total = uncleaved_seqs+middle_seqs+cleaved_seqs
            list_floats[seq] = float(cleaved_seqs)/total
    return list_floats

def generate_random_seqs(length_seq):
    for string in itertools.imap(''.join, itertools.product('ACDEFGHIKLMNPQRSTVWY', repeat=length_seq)):
        yield string
