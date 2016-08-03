import sys
import numpy
import math
from itertools import product

def readSpecProfile( filename ):
    with open(filename) as transfac_file:
        transfac = transfac_file.readlines()

    motifWidth = len(transfac)-2

    aaAlpha = transfac[1].split()[1:]

    freq = [{k: 0.0 for k in aaAlpha} for i in range(motifWidth)]

    t_read = transfac[2:]

    for pos,line in enumerate( t_read,0 ):
        for aa_ind,f in enumerate( line.split()[1:], 0):
            freq[pos][aaAlpha[aa_ind]] = float(f)
    return freq

def main(args):
    #read in and rename arguments
    inTransfacFile=args[1]
    outfile=args[2]
    rep=int(args[3])
    #    inSeqsFile=args[2]

    #make a name for the score file
    #tokens=inSeqsFile.rsplit('.',1)
    #file=tokens[0]
    #outfile= '%s_score.txt' % (file)
    
    #this is the representation of a transfac.  It is a list of dictionaries - each item in the list holds one dictionary for each position
    #each dictionary holds one item per amino acid, the key for the dict is the one letter code for the amino acid and the value is the probability
    freq_in = readSpecProfile( inTransfacFile )
    
    #your code
    #read in list of seqs
    #with open(inSeqsFile) as seqs_file:
    #    seqsList = seqs_file.readlines()

    alphabet=['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y']
    seqsList = (''.join(i) for i in product(alphabet, repeat = rep))
        
    scoresList = []
    
    dist_out = open(outfile,"w")

    #loop through seqs, for each seq generate score using freq_in
    for seq in seqsList:
        score = numpy.sum( [ freq_in[pos][letter] for pos,letter in enumerate( seq.strip(),0 ) if freq_in[pos][letter] != 0.0 ] )

        dist_out.write("%s\t%s\n" % (seq.strip(),score))
 
    dist_out.close()
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
