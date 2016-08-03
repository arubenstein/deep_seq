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

    
    #seqfile, if list of seqs is given then kick off all at a time. interval is > than the total number of sequences. ncores = 1000. server_num = 1.

    counter = 0
 
    #folder_names = glob.glob("{outpath}miseq_nextseq_seqs_*".format(outpath=OUTPATH))

    with open(seqfile) as s:
        lines = s.readlines()

    #folder_seqs = dict( (os.path.split(os.path.splitext(fn)[0])[1],[]) for fn in folder_names )
    folder_seqs = {}
    for line in lines:
        if folder_seqs.get(line[0:3]) is None:
            folder_seqs[line[0:3]] = []
        folder_seqs[line[0:3]].append(line.strip())

    for folder, seqs in folder_seqs.items():
	sfn = os.path.join(OUTPATH, folder, folder)
	if not os.path.isfile(sfn):
	    continue 
	len_pdb = len(glob.glob(os.path.join(OUTPATH, folder, "*.pdb")))
        if len_pdb == len(seqs):
	    continue
		
        counter = counter+1
	print counter
        seq_list = ""

	#if seqs:
	    #write the names of the sequences
        #    seq_list = os.path.join(OUTPATH, folder, "seqs.list") 
        #    with open(seq_list, 'w') as out:
	#	out.writelines('%s\n' % (i) for i in seqs)

	#generic command
        command = "{scripts}/extract.sh {f} {sl}".format( scripts=SCRIPTS, sl=seq_list, f=sfn )
	    
	#if slurm style, write script and run as a batch script
        job_count=int(math.ceil(counter/180.0))
        script_fn = "{o}{c}.{suff}".format(o=OUTPATH, c=job_count, suff='qsub')

	with open(script_fn, 'a') as script:
	    header = "#!/bin/bash\n#PBS -l nodes=1\n#PBS -l walltime=6:00:00\n#PBS -q tyr\n#PBS -N {c}\n#PBS -o {outpath}/{c}.out\n#PBS -e {outpath}/{c}.err\n".format(c = job_count, outpath=OUTPATH)
	    str_counter = str(counter)    
	    #if queue_type is slurm or queue_type is torque and it's the first of 192 commands then write a header to the script
	    if counter % 180 == 1:
		script.write(header)

	    script.write(command + " &\n")
            if counter % 30 == 0:
		script.write("\nwait\n")
	    if counter % 180 == 0:
                p = Popen("qsub " + script_fn, shell=True)
	        #pass
		#manually add wait and qsub last script
    print counter
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--seq_file', default="", help="Optional, can input a sequences file - each sequence will be run on its own")
    args = parser.parse_args()

    main(args.seq_file) 
