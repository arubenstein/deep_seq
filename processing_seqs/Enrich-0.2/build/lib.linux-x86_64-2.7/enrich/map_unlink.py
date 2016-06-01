#!/usr/bin/env python
'''
map_unlink: the map_unlink module uses unique variant counts generated by map_counts to calculate unlinked mutation frequencies for all possible single mutants from all variants. 

Variants with multiple mutations are unlinked; the variant frequency is added to each of the single mutants comprising the multiply mutated variant.  Map_unlink can be invoked in multipe modes.  Currently supported modes are counts and wild_counts. The difference between counts and wild_counts is that, for counts only positions that differ from wild type (i.e. mutations) are ennumerated whereas for wild_counts, all positions for each variant are included in the calculation regardless of the identity of the amino acid. In other words, in counts mode the map_unlink calculation at each position yields the frequency of mutants amino acids only whereas the wild_counts mode yields frequency information for all amino acids. Note that this module contains many currently undocumented modes other than wild_counts and counts. They are fully functional but have not been extensively tested.
'''

import sys, os, time #import standard libraries

__author__ = "Douglas M. Fowler"
__copyright__ = "Copyright 2011"
__credits__ = ["Douglas M Fowler", "Carlos L. Araya"]
__license__ = "FreeBSD"
__version__ = "0.2"
__maintainer__ = "Douglas M. Fowler"
__email__ = "dfowler@uw.edu"

def main(path, infile, molecule, mode, size, grid = 'L'):

    if grid != 'L':
        print time.asctime(time.localtime())
        print path, infile, molecule, mode, size
    
    try:
        #set input path and output file:
        f_infile = open(path + 'data/output/' + infile, 'U')
        f_outfile = open(path + 'data/output/' + 'unlink' + '_' + mode + '_' + infile.split('_', 1)[1], 'w')
    
    except:
        print 'Error: could not open input file'
        return 1
    
    try:
        size = int(size)
            
    except:
        print 'Error: integer-only parameters were not integers'
        return 1
    
    #set characters for molecule type:
    symbols = []
    if molecule == 'PRO':
        symbols = ['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y','*']
        
    elif molecule == 'DNA':
        symbols = ['A','T','G','C']
    
    else:
        print 'Error: molecule type invalid'
        return 1    
    #print the header:
    print >> f_outfile, '\t'.join(['position'] + symbols)
    
    #generate keys for internal dictionary:
    l = f_infile.readline()
    data = {}
    for i in range(0,size):
        data[i] = {}
        for symbol in symbols:
            data[i][symbol] = []
    
    while l:
        l = f_infile.readline()
        line = l.rstrip().split('\t')
            
        if len(line) > 4 and mode == "wild_counts":
            sequence, y, empty = line[1], float(line[7]), 0
            x = 0
            for symbol in sequence:
                try:
                    data[x][symbol].append(y)
                    
                except KeyError:
                    data[x][symbol] = [y]
                x += 1
        
        elif len(line) > 4 and 'multiple_map' in mode:
            
            if 'wild' in mode:
                sequence, y, empty = line[1], float(line[6]), 0
                x = 0
                
                for symbol in sequence:
                
                    if data[x].has_key(symbol):
                        data[x][symbol].append(y)
                    
                    else:
                        data[x][symbol] = [y]
                    x += 1
    
            elif line[0] != 'NA-NA':
                location = map(int, line[0].split('-')[0].split(','))
                id = line[0].split('-')[1].split(',')
                y, empty = float(line[6]), 0
                
                for x in location:
                    symbol = id.pop(0)
                    if data[x].has_key(symbol):
                        data[x][symbol].append(y)
                        
                    else:
                        data[x][symbol] = [y]
                    
        elif len(line) > 4 and 'difference' in mode and line[2] != 'NA':
            location = map(int, line[2].split(','))
            id = line[3].split(',')
            
            if 'difference_log2' in mode:
                y, empty = float(line[10]), 'NA'
                
            if 'difference_wt' in mode:
                y, empty = float(line[11]), 'NA'
                
            for x in location:
                symbol = id.pop(0)
                if data[x].has_key(symbol):
                    data[x][symbol].append(y)
                else:
                    data[x][symbol] = [y]
            
        elif len(line) > 4 and not line[4] == 'NA' and 'difference' not in mode:
            location = map(int, line[4].split(','))
            id = line[5].split(',')
            
            if mode == 'counts': 
                y, empty = float(line[7]), 0
            
            elif mode == 'unique':
                y, empty = 1, 0
                            
            elif mode == 'ratios': 
                y, empty = float(line[7]), "NA"
    
            elif mode == 'dnaratio':
                y, empty = float(line[14]), "NA"
    
            elif mode == 'dnastdev':
                y, empty = float(line[15]), "NA"
    
            elif mode == 'rosetta':
                y, empty = float(line[13]), "NA"
    
            for x in location:
                symbol = id.pop(0)
                try:
                    data[x][symbol].append(y)
                
                except KeyError:
                    data[x][symbol] = [y]
    
    abssum = 0
    maxabssum = 0
    
    if 'sum_absval' in mode:
        for x in range(0,size):
            
            for symbol in symbols:
                values = data[x][symbol]
                abssum = sum(map(abs, values))
                data[x][symbol] = abssum
                
                if maxabssum < abssum:
                    maxabssum = abssum
                
        for x in range(0,size):
            string = [str(x)]
            
            for symbol in symbols:
                
                if data[x][symbol] == 0:
                    string.append(empty)
                
                else:
                    string.append(data[x][symbol]/maxabssum)
            
            print >> f_outfile, '\t'.join(map(str, string))
                
    else:
        for x in range(0,size):
            string = [str(x)]
            for symbol in symbols:
                values = data[x][symbol]
                if values == []:
                    string.append(empty)
                    
                elif mode in ["counts", "unique", "wild"] or 'sum' in mode or 'wild_sum' in mode or 'counts' in mode: 
                    string.append(sum(values))
                
                elif mode in ["ratios", "rosetta"] or 'average' in mode or 'wild_average' in mode:
                    string.append(float(sum(values))/len(values))
                
                elif mode in ["dnaratio", "dnastdev"]:
                    string.append(sum(values))
                
            print >> f_outfile, '\t'.join(map(str, string))
    
    f_outfile.close()
    return(0)
            
if __name__ == '__main__':
    
    import optparse
    print time.asctime(time.localtime())    

    parser = optparse.OptionParser()
    parser.add_option('--molecule', action = 'store', type = 'string', dest = 'molecule', help = 'DNA or PRO')
    parser.add_option('--path', action = 'store', type = 'string', dest = 'path', help = 'path from script to files')
    parser.add_option('--infile', action = 'store', type = 'string', dest = 'infile', help = 'input file, is either mapCounts or mapRatios data')
    parser.add_option('--mode', action = 'store', type = 'string', dest = 'mode', help = 'should I use a per sequence counts column?')
    parser.add_option('--size', action = 'store', type = 'int', dest = 'size', help = 'length of input sequence (DNA or PRO)')
    parser.add_option('--local', action = 'store', type = 'string', dest = 'local', help = 'Is this a local (L) run or should an SGE (SGE) job be scheduled?')
    (option, args) = parser.parse_args()
    
    main(option.path, option.infile, option.molecule, option.mode, option.size, option.local)
    
    print time.asctime(time.localtime())