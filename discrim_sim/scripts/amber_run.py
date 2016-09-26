#!/usr/bin/env python

import os
import sys
import argparse
import itertools
import math
from subprocess import Popen
import glob
from shutil import copy 

OUTPATH="/scratch/alizarub/git_repos/deep_seq/discrim_sim/results/"
INPATH="/home/alizarub/git_repos/deep_seq/discrim_sim/input/"
SCRIPTS="/home/alizarub/git_repos/deep_seq/discrim_sim/scripts/"
ROSETTA_BIN="/home/alizarub/Rosetta/main/source/bin/"
ROSETTA_DB="/home/alizarub/Rosetta/main/database/"
XML="/home/alizarub/git_repos/deep_seq/discrim_sim/xml/"

def main(seqfile, queue_type):

    
    counter = 0
    counter_complete = 0
    counter_dat_0 = 0

    if queue_type == "slurm":
        njobs_per_core = 50
        bg = ""
        script_suff = "sbatch"
    elif queue_type == "torque":
        njobs_per_core = 210
        bg = '&'
        script_suff = "qsub"
 
    list_pdbs = glob.glob(OUTPATH + '/*/*.pdb')

    for pdb in list_pdbs:

	with open(pdb) as p:
	    if "ATOM" not in p.read():
                continue

	seq = os.path.split(os.path.splitext(pdb)[0])[1]
	path = os.path.split(pdb)[0]

	dat = os.path.join(path, seq + "_dat_binding")

	if os.path.isfile(dat) and os.path.getsize(dat) > 0:
	    with open(dat) as d:
                x = d.read()
		if float(x.strip()) != 0:
	            counter_complete = counter_complete + 1
	            continue
		else:
		    counter_dat_0 = counter_dat_0 + 1

	counter = counter+1
	'''
	#generic command
        command = "{scripts}/amber_run_file.sh {p} {path} > {path}/{p}_amber.log".format( scripts=SCRIPTS, p=seq, path=path )
	    
        #if slurm style, write script and run as a batch script
        job_count=int(math.ceil(counter/float(njobs_per_core)))
        script_fn = "{o}{c}amber.{suff}".format(o=OUTPATH, c=job_count, suff=script_suff)

        with open(script_fn, 'a') as script:
            if queue_type == "torque":
                header = "#!/bin/bash\n#PBS -l nodes=1\n#PBS -l walltime=6:00:00\n#PBS -q tyr\n#PBS -N {s}amber\n#PBS -o {p}/{s}amber.out\n#PBS -e {p}/{s}amber.err\n".format(p=path, s=seq, outpath=OUTPATH)
            elif queue_type == "slurm":
                header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --time=1:30:00\n#SBATCH --job-name={c}amber\n#SBATCH -o {outpath}/slurm{c}amber.out\n\n".format(c=job_count, outpath=OUTPATH)
            #if queue_type is slurm or queue_type is torque and it's the first of 192 commands then write a header to the script
            if counter % njobs_per_core == 1:
                script.write(header)

            script.write(command + " " + bg + "\n")
            if queue_type == "torque" and counter % 30 == 0:
                script.write("\nwait\n")
            if counter % njobs_per_core == 0:
                #p = Popen(script_suff + " " + script_fn, shell=True)
                pass '''
                #manually add wait and qsub last script

    print counter
    print counter_complete
    print counter_dat_0
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', default="", help="Optional, can input a sequences file - each sequence will be run on its own")
    parser.add_argument ('--queue_type', default="", help="slurm or torque")
    
    args = parser.parse_args()

    main(args.seq_file, args.queue_type) 
