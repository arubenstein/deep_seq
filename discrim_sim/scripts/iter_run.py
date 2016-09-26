#!/usr/bin/env python


import os
import argparse
import itertools
import math
from subprocess import Popen
import glob

def main(server_num, queue_type, fen2, test_complete):

    #3 possible server cases
    #1. bash style, run 4000 jobs on 58 cores each on 7 gaann servers. interval = 4000/7. ncores = 58.
    #2. slurm style, run as slurm batch script and kick off 1000 jobs. interval = 1000. ncores = N/A
      #2a. fen2, add sbatch comments about this. interval = 1000. ncores = N/A.
    #3. torque style, run as torque batch script and kick off 500 jobs (on 20 nodes, 24 processes each). interval = 500. ncores = N/A

    
    #if bash style server num is between 8 and 14
    #if slurm style server num is between 1 and 4 (each runs 1000 jobs between 0 and 4000 )
    #if torque style server num is between 31 and 32 (7501-8000)

    counter = 0
 
    if queue_type == "torque":
        interval = 250 
        script_suff = "qsub"
        a_or_w = 'a'
        background = "&"
	#script_pre=" -q long "
        script_pre=""
    elif queue_type == "slurm":
        interval = 1000
        script_suff = "sbatch"
        a_or_w = 'w'
        background = ""
	script_pre = ""
    else:
	interval = math.ceil(8000/14.0) #this is the number of jobs that this script should kick off in total
        ncores = 58

    ps = []    

    #set list_seqs according to whether or not seqfile is present.
    list_seqs = [ string for string in itertools.imap(''.join, itertools.product('ACDEFGHIKLMNPQRSTVWY', repeat=3)) ]

    for item in list_seqs:
        counter = counter+1

        if interval*(server_num-1) < counter <= interval*server_num:
	    prefix = item
	        
	    #if this was already run 
	    #does not test that _dat_complex is not empty (or 0)
	    if test_complete and len(glob.glob("{outpath}{prefix}/{prefix}*_dat_complex".format(outpath=OUTPATH, prefix=prefix))) == 400:
	        continue
	    
            try:
	        os.mkdir(OUTPATH + prefix)
	    except:
		pass

	    #generic command
            command = "{s}/rosetta_amber_seq.sh {bin} {db} {inpath} {temppath} {outpath} {p} {home} {s} {torque}".format( bin=ROSETTA_BIN, db=ROSETTA_DB, temppath=TEMPPATH, outpath=OUTPATH, inpath=INPATH, p=prefix, s=SCRIPTS, home=home, torque='fen2' if fen2 else queue_type )
	    
	    #if slurm style, write script and run as a batch script
            if queue_type != "bash":
                if queue_type == "slurm":
                    script_fn = OUTPATH + prefix + '/' + prefix + "." + script_suff
                elif queue_type == "torque": 
                    job_count=int(math.ceil(counter/24.0))
                    script_fn = "{o}{c}.{suff}".format(o=OUTPATH, c=job_count, suff=script_suff)

	        with open(script_fn, a_or_w) as script:
		    if fen2:
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --export=ALL\n#SBATCH --job-name={p}\n#SBATCH -p main\n#SBATCH -o {outpath}{p}/slurm{p}.out\n#SBATCH -t 60:00:00\n#SBATCH --mem=5500\n\n".format(p = prefix,outpath=OUTPATH)
		    elif queue_type == "slurm":
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --export=ALL\n#SBATCH --job-name={p}\n#SBATCH -o {outpath}{p}/slurm{p}.out\n\n".format(p = prefix, outpath=OUTPATH)
                    elif queue_type == "torque": 
			header = "#!/bin/bash\n#PBS -l nodes=1\n#PBS -l walltime=24:00:00\n#PBS -q tyr\n#PBS -N {c}\n#PBS -o {outpath}/{c}.out\n#PBS -e {outpath}/{c}.err\n".format(c = job_count, outpath=OUTPATH)
		    
		    #if queue_type is slurm or queue_type is torque and it's the first of 24 commands then write a header to the script
		    if queue_type == "slurm" or counter % 24 == 1:
                        script.write(header)
		    script.write(command + " > {outpath}{p}/{p}.log {bg}\n".format( outpath=OUTPATH, p=prefix, bg=background ))
                    if queue_type == "slurm" or counter % 24 == 0 or counter == len(list_seqs):
                        if queue_type == "torque":
			    script.write("\nwait\n")
	                p = Popen(script_suff + script_pre + " " + script_fn, shell=True)

	    #if bash style, run as a process and wait at the end
	    else:
	        with open(OUTPATH + prefix + '/' + prefix + ".log", 'w') as file_out:
            	    p = Popen("nohup nice " + command, stdout=file_out, shell=True)
                ps.append(p)
        
                if len(ps) >= ncores:
                    for p in ps:
                        p.wait()
	            ps = []

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument ('--server_num', type=float, help="server id out of 7 servers")
    parser.add_argument ('--queue_type', choices=["torque", "bash", "slurm"], help="is this being run as bash, slurm, or torque job")
    parser.add_argument ('--fen2', dest='fen2', action='store_true', help="is this being run on fen2. if yes, change some of sbatch headers")
    parser.add_argument ('--no-fen2', dest='fen2', action='store_false', help="is this being run on fen2. if yes, change some of sbatch headers")
    parser.add_argument ('--test-complete', dest='test_complete', action='store_true', help="should the folders be tested for the existence of 400 dat files.  Only set to true if sure that amber is running correctly.")
    parser.add_argument ('--no-test-complete', dest='test_complete', action='store_false', help="should the folders be tested for the existence of 400 dat files.  Only set to true if sure that amber is running correctly.")
    args = parser.parse_args()

    global OUTPATH
    global INPATH
    global SCRIPTS
    global ROSETTA_BIN
    global ROSETTA_DB
    global XML
    global TEMPPATH

    main_path="/git_repos/deep_seq/discrim_sim/"
    if args.queue_type == "torque":
	home="/home/arubenstein"
        TEMPPATH="$TMPDIR"
    elif args.queue_type == "slurm":
	home="/home/alizarub"
        TEMPPATH="/scratch/alizarub" + main_path + "results/"
    elif args.queue_type == "bash":
	home="/home/arubenstein"
        TEMPPATH=home + main_path + "results/"

    OUTPATH = home + main_path + "results/"
    INPATH = home + main_path + "input/" 
    SCRIPTS = home + main_path + "scripts/" 
    ROSETTA_BIN = home + "/Rosetta/main/source/bin/"
    ROSETTA_DB = home + "/Rosetta/main/database/"
    XML = home + main_path + "xml/"

    main(args.server_num, args.queue_type, args.fen2, args.test_complete) 
