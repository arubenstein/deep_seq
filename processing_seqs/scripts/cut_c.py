import time 
import sys
import os
from itertools import groupby

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

def comp_seq( fasta_seq, WT_seq ):
    if len(fasta_seq.strip()) <= 128:
	return None
    
    nomatch=False    
   
    for f,wt in zip(fasta_seq, WT_seq):
        if ( wt != "X" and f != wt ):
	    nomatch=True
	    break

    if not nomatch:
	final_seq = fasta_seq
    else:
        WT_augment= "C" + WT_seq
        nomatch=False

        for f,wt in zip(fasta_seq, WT_augment):
	    if ( wt != "X" and f != wt ):
	        nomatch=True
	        break

        if nomatch or len(fasta_seq)==129:
	    final_seq = None
        else:
	    final_seq = fasta_seq[1:]
    return final_seq
	
def write_fasta( outfile, header, seq ):
    outfile.write(">%s\n" % header)
    outfile.write(seq + "\n")

def main( argv ):

    infile = argv[1]

    filename = infile.rsplit(".",1)[0]

    output_file = '%s_cut.fasta' % (filename)

    err_file = '%s_nomatch.fasta' % (filename)

    WT_seq = "GTTCCAGACTACGCTCTGCAGGCTAGTGGTGGAGGAGGCTCTGGTGGAGGCGGTAGCGGAGGCGGAGGGTCGXXXXXXXXXXXXXXXTGTGCTTCTCATTTGGGCAGTGATTATAAAGATGATGATGAT"

    #open the files for input and output
    fasta_sequences = fasta_iter(infile)
    with open(output_file,"w") as out_file:
	with open(err_file,"w") as err:
	    for name,sequence in fasta_sequences:
                if name == "dummy":
		    continue
		new_sequence = comp_seq ( sequence, WT_seq )
                if new_sequence:
	            write_fasta(out_file, name, new_sequence )
	        else:
		    write_fasta( err, name, sequence )

if __name__ == "__main__":
    main(sys.argv)

