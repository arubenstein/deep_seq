#!/usr/bin/env python

import os
import sys
import argparse
import itertools
import math
from subprocess import Popen
import glob
from shutil import copy 

OUTPATH="/home/arubenstein/git_repos/deep_seq/discrim_sim/results/"
INPATH="/home/arubenstein/git_repos/deep_seq/discrim_sim/input/"
SCRIPTS="/home/arubenstein/git_repos/deep_seq/discrim_sim/scripts/"
ROSETTA_BIN="/home/arubenstein/Rosetta/main/source/bin/"
ROSETTA_DB="/home/arubenstein/Rosetta/main/database/"
XML="/home/arubenstein/git_repos/deep_seq/discrim_sim/xml/"

def main(seqfile):

    
    counter = 0
 
    list_pdbs = glob.glob(OUTPATH + '/*/*.pdb')

    for pdb in list_pdbs:
        counter = counter+1

	#generic command
        command = "{scripts}/amber_run_file.sh {p} {path} > {path}{p}_amber.log".format( scripts=SCRIPTS, p=os.path.split(os.path.splitext(pdb)[0])[1], path=os.path.split(pdb)[-2] )
	    
	#if slurm style, write script and run as a batch script
        job_count=int(math.ceil(counter/210.0))
        script_fn = "{o}{c}amber.{suff}".format(o=OUTPATH, c=job_count, suff='qsub')

	with open(script_fn, 'a') as script:
	    header = "#!/bin/bash\n#PBS -l nodes=1\n#PBS -l walltime=6:00:00\n#PBS -q tyr\n#PBS -N {c}amber\n#PBS -o {outpath}/{c}amber.out\n#PBS -e {outpath}/{c}amber.err\n".format(c = job_count, outpath=OUTPATH)
	    str_counter = str(counter)    
	    #if queue_type is slurm or queue_type is torque and it's the first of 192 commands then write a header to the script
	    if counter % 210 == 1:
		script.write(header)

	    script.write(command + " &\n")
            if counter % 30 == 0:
		script.write("\nwait\n")
	    if counter % 210 == 0:
                #p = Popen("qsub " + script_fn, shell=True)
	        pass
		#manually add wait and qsub last script
    print counter
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', default="", help="Optional, can input a sequences file - each sequence will be run on its own")
    args = parser.parse_args()

    main(args.seq_file) 
