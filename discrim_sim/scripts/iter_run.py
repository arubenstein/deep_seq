#!/usr/bin/env python

import os
import sys
import argparse
import itertools
import math
from subprocess import Popen

OUTPATH="/scratch/alizarub/git_repos/deep_seq/discrim_sim/results/"
INPATH="/home/alizarub/git_repos/deep_seq/discrim_sim/input/"
SCRIPTS="/home/alizarub/git_repos/deep_seq/discrim_sim/scripts/"
ROSETTA_BIN="/home/alizarub/Rosetta/main/source/bin/"
ROSETTA_DB="/home/alizarub/Rosetta/main/database/"
XML="/home/alizarub/git_repos/deep_seq/discrim_sim/xml/"

def main(server_num, slurm, fen2, seqfile):

    #4 possible use cases
    #1. bash style, run 2000 jobs on 58 cores each on 7 gaann servers. interval = 2000/7. ncores = 58.
    #2. slurm style, run as slurm batch script and kick off 1000 jobs. interval = 1000. ncores = N/A
      #2a. fen2, add sbatch comments about this. interval = 1000. ncores = N/A.
      #2b. seqfile, if list of seqs is given then kick off 1000 at a time interval is > than the total number of sequences. ncores = 1000. server_num = 1.
      #2b. this should only be run on fen or fen2.

    #if bash style server num is between 1 and 7
    #if slurm style server num is between 5 and 8 (each runs 1000 jobs between 4000 and 8000 )
    counter = 0
 
    if seqfile != "" and slurm == "true":
        interval = 1000
	wait = False
	ncores = 1000
    elif slurm == "true":
        interval = 1000
        wait = False
	ncores = 1000
    else:
	interval = math.ceil(8000/14.0) #this is the number of jobs that this script should kick off in total
    	wait = True
        ncores = 58

    ps = []    

    #set list_seqs according to whether or not seqfile is present.
    if seqfile == "":
        list_seqs = ( string for string in itertools.imap(''.join, itertools.product('ACDEFGHIKLMNPQRSTVWY', repeat=3)) )
    else:
        with open(seqfile) as s:
            lines = s.readlines()
        seqs = [ l.strip() for l in lines ]
        step = int(math.ceil(len(seqs)/1000.0))
        list_seqs = ( seqs[start:start+step] for start in xrange(0, len(seqs), step) ) 

    for item in list_seqs:
        counter = counter+1

        if interval*(server_num-1) < counter <= interval*server_num:
	    if seqfile == "":
	        prefix = item
                fragfiles = ""
	        #if this was already run 
	        #test that ? works as expected
	        if len(glob.glob("{outpath}{prefix}/{prefix}??.pdb".format)) == 400:
                    continue
	    else:
                prefix = "{list_fn}_{c}".format(list_fn=os.path.split(os.path.splitext(seqfile)[0])[1], c=counter)
                list_name = "{outpath}/{p}/{p}.list".format( outpath=OUTPATH, p=prefix )
	        fragfiles = " -in::file::frag_files {l}".format( l=list_name )
	    
            try:
	        os.mkdir(OUTPATH + prefix)
	    except: 
	        pass

	    if seqfile != "":
	        #write the names of the sequences
                with open(list_name,'w') as out:
                    out.writelines('%s\n' % (i) for i in item)

	    #generic command
            command = "{bin}/discrim_sim.static.linuxgccrelease -database {db} -s {inpath}/pdbs/Job_20ly104_0032.pdb -out::path::pdb {outpath}/{prefix}/ -enzdes::cstfile {inpath}/pdbs/ly104cstfile.txt -run:preserve_header @/home/alizarub/git_repos/general_src/enzflags -out::prefix {prefix} -resfile {inpath}/resfile/rfpackpept.txt {f}".format( bin=ROSETTA_BIN, db=ROSETTA_DB, outpath=OUTPATH, inpath=INPATH, prefix=prefix, f=fragfiles )
	    
	    #if slurm style, write script and run as a batch script
            if slurm == "true":
	        with open(OUTPATH + prefix + '/' + prefix + ".sbatch", 'w') as script:
		    if fen2 == "true":
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --job-name={p}\n#SBATCH -p main\n#SBATCH --export=ALL\n#SBATCH -o {outpath}{p}/slurm{s}.out\n#SBATCH --time=30:00:00\n".format(p = prefix,outpath=OUTPATH)
		    else:
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --job-name={p}\n#SBATCH -o {outpath}{p}/slurm{p}.out\n\n".format(p = prefix, outpath=OUTPATH)
		    script.write(header)
		    script.write(command + " > {outpath}{p}/{p}.log".format( outpath=OUTPATH, p=prefix ))
	        p = Popen("sbatch {outpath}{p}/{p}.sbatch".format(outpath=OUTPATH, p=prefix ), shell=True)

	    #if bash style, run as a process and wait at the end
	    else:
	        with open(OUTPATH + prefix + '/' + prefix + ".log", 'w') as file_out:
            	    p = Popen("nohup nice " + command, stdout=file_out, shell=True)
	    
            ps.append(p)
        
        if wait and len(ps) >= ncores:
            for p in ps:
                p.wait()
	    ps = []

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--server_num', type=float, help="server id out of 7 servers")
    parser.add_argument ('--slurm', help="is this being run as slurm job")
    parser.add_argument ('--fen2', default="false", help="is this being run on slurm2. if yes, change some of sbatch headers")
    parser.add_argument ('--seq_file', default="", help="Optional, can input a sequences file - each sequence will be run on its own")
    args = parser.parse_args()

    main(args.server_num, args.slurm, args.fen2, args.seq_file) 