#!/usr/bin/env python

def hamdist(str1, str2):
    '''Determines hamming distance between two strings'''
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs
