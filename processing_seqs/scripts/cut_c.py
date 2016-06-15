import time 
import sys
import os
from itertools import groupby
import argparse

def fasta_iter(fasta_name):
    """
    given a fasta file. yield tuples of header, sequence
    """
    fh = open(fasta_name)
    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        # drop the ">"
        header = header.next()[1:].strip()
        # join all sequence lines to one.
        seq = "".join(s.strip() for s in faiter.next())
        yield header, seq

def comp_seq_miseq( fasta_seq, WT_seq ):
    
    #make sure this is long enough
    if len(fasta_seq.strip()) <= 128:
	return None
    
    nomatch=False    
   
    #check if entire string matches perfectly
    for f,wt in zip(fasta_seq, WT_seq):
        if ( wt != "X" and f != wt ):
	    nomatch=True
	    break

    #if it does match, you're done
    if not nomatch:
	final_seq = fasta_seq
    #if not, add a "C" to the beg of the WT_seq and check if entire string matches perfectly
    else:
        WT_augment= "C" + WT_seq
        nomatch=False

        for f,wt in zip(fasta_seq, WT_augment):
	    if ( wt != "X" and f != wt ):
	        nomatch=True
	        break
	#if it doesn't match perfectly or its length is 129 (1 more than 128, which is what we want for the sequence starting in GTTC) throw it out
        if nomatch or len(fasta_seq)==129:
	    final_seq = None
	#otherwise, take the entire sequence starting from the second base
        else:
	    final_seq = fasta_seq[1:]
    return final_seq

def comp_seq_nextseq( fasta_seq, WT_seq ):
    #check if "TCTTTATAA" is found in the seq
    match_seq="TCTTTATAA"
    WT_index=WT_seq.find(match_seq)
    index=fasta_seq.find(match_seq)

    #if no, throw out
    if index == -1:
        final_seq = None
    #if yes, pad its beginning and end to match WT_seq
    else:
	if WT_index > index:
	    prefix = WT_seq[0:WT_index-index]
            fasta_seq = prefix + fasta_seq
	else:
	    fasta_seq = fasta_seq[index-WT_index:]
        final_seq = fasta_seq
        #doesn't contain the library region
	if len(fasta_seq) < 66:
	    final_seq = None
	#basically always as nextseq is usually around 70-80 bp
	elif len(fasta_seq) < len(WT_seq):
	    suffix = WT_seq[len(fasta_seq):len(WT_seq)]
            fasta_seq = fasta_seq + suffix
            final_seq = fasta_seq
	count_error = 0
        N_count = 0
        #check if matches perfectly
        for f, wt in zip(fasta_seq, WT_seq):
            if wt != "X" and f != wt :
		count_error = count_error + 1
	    if f == "N":
	        N_count = N_count + 1
	if count_error >= 1:
	    final_seq = None
	if N_count >= 1:
	    final_seq = None

    if final_seq is not None:
        final_seq = rev_comp(final_seq)

    return final_seq
	
def rev_comp(seq):
    seq_dict = {'A':'T','T':'A','G':'C','C':'G'}
    return "".join([seq_dict[base] for base in reversed(seq)])
	
def write_fasta( outfile, header, seq ):
    outfile.write(">%s\n" % header)
    outfile.write(seq + "\n")

def main( infile, nextseq, outpath ):

    filename = os.path.splitext(os.path.basename(infile))[0]

    output_file = '%s/%s_cut.fasta' % (outpath, filename)

    err_file = '%s/%s_nomatch.fasta' % (outpath, filename)

    if nextseq:
        WT_seq = "ATCATCATCATCTTTATAATCACTGCCCAAATGAGAAGCACAXXXXXXXXXXXXXXXCGACCCTCCGCCTCCGCTACCGCCTCCACCAGAGCCTCCTCCACCACTAGCCTGCAGAGCGTAGTCTGGAAC"
    else:
        WT_seq = "GTTCCAGACTACGCTCTGCAGGCTAGTGGTGGAGGAGGCTCTGGTGGAGGCGGTAGCGGAGGCGGAGGGTCGXXXXXXXXXXXXXXXTGTGCTTCTCATTTGGGCAGTGATTATAAAGATGATGATGAT"

    #open the files for input and output
    fasta_sequences = fasta_iter(infile)
    with open(output_file,"w") as out_file:
	with open(err_file,"w") as err:
	    for name,sequence in fasta_sequences:
                if name == "dummy":
		    continue
		if nextseq:
		    new_sequence = comp_seq_nextseq ( sequence, WT_seq )
                else:
		    new_sequence = comp_seq_miseq( sequence, WT_seq )
		if new_sequence:
	            write_fasta(out_file, name, new_sequence )
	        else:
		    write_fasta( err, name, sequence )

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--infile', help="name of fasta input file with full path")
    parser.add_argument ('--nextseq', default=False, help="is this nextseq data?")
    parser.add_argument ('--outpath', help="Path for output files")

    args = parser.parse_args()

    main(args.infile, args.nextseq, args.outpath)
