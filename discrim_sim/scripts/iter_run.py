#!/usr/bin/env python

import os
import sys
import argparse
import itertools
import math
from subprocess import Popen

OUTPATH="/home/arubenstein/git_repos/deep_seq/discrim_sim/results/"
INPATH="/home/arubenstein/git_repos/deep_seq/discrim_sim/input/"
SCRIPTS="/home/arubenstein/git_repos/deep_seq/discrim_sim/scripts/"
ROSETTA_BIN="/home/arubenstein/Rosetta/main/source/bin/"
ROSETTA_DB="/home/arubenstein/Rosetta/main/database/"
XML="/home/arubenstein/git_repos/deep_seq/discrim_sim/xml/"

def main(server_num, slurm):

    #if bash style server num is between 1 and 7
    #if slurm style server num is between 5 and 8 (each runs 1000 jobs between 4000 and 8000 )
    counter = 0
 
    if slurm == "true":
        interval = 1000
    else:
	interval = math.ceil(8000/14.0) #this is the number of jobs that this script should kick off in total
    ncores = 58
    ps = []    

    for string in itertools.imap(''.join, itertools.product('ACDEFGHIKLMNPQRSTVWY', repeat=3)):
        counter = counter+1

        if interval*(server_num-1) < counter <= interval*server_num:
	    os.mkdir(OUTPATH + string)
	    #generic command
            command = "nohup nice {bin}/discrim_sim.static.linuxgccrelease -database {db} -s {inpath}/pdbs/Job_20ly104_0032.pdb -out::path::pdb {outpath}/{s}/ -enzdes::cstfile {inpath}/pdbs/ly104cstfile.txt -run:preserve_header @/home/arubenstein/git_repos/general_src/enzflags -out::prefix {s} -resfile {inpath}/resfile/rfpackpept.txt".format( bin=ROSETTA_BIN, db=ROSETTA_DB, outpath=OUTPATH, inpath=INPATH, s=string )
	    
	    #if slurm style, write script and run as a batch script
            if slurm == "true":
	        with open(OUTPATH + string + '/' + string + ".sbatch", 'w') as script:
		    header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --job-name={s}\n\n".format(s = string)
		    script.write(header)
		    script.write(command + " > {outpath}{s}/{s}.log".format( outpath=OUTPATH, s=string ))
	        p = Popen("slurm {outpath}{s}/{s}.sbatch".format(outpath=OUTPATH, s=string ))
	    #if bash style, run as a process and wait at the end
	    else:
	        with open(OUTPATH + string + '/' + string + ".log", 'w') as file_out:
            	    p = Popen(command, stdout=file_out, shell=True)
		    ps.append(p)

	#will never be true for slurm style
        if len(ps) >= ncores:
            for p in ps:
                p.wait()
	    ps = []

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--server_num', type=float, help="server id out of 7 servers")
    parser.add_argument ('--slurm', help="is this being run as slurm job")
    args = parser.parse_args()

    main(args.server_num, args.slurm) 
