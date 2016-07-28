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

def main(server_num, queue_type, fen2, seqfile):

    #3 possible server cases
    #1. bash style, run 2000 jobs on 58 cores each on 7 gaann servers. interval = 2000/7. ncores = 58.
    #2. slurm style, run as slurm batch script and kick off 1000 jobs. interval = 1000. ncores = N/A
      #2a. fen2, add sbatch comments about this. interval = 1000. ncores = N/A.
    #3. torque style, run as torque batch script and kick off 1000 jobs. interval = 1000. ncores = N/A

    
    #seqfile, if list of seqs is given then kick off all at a time interval is > than the total number of sequences. ncores = 1000. server_num = 1.

    #if bash style server num is between 1 and 7
    #if slurm style server num is between 5 and 8 (each runs 1000 jobs between 4000 and 8000 )
    #if torque style server num is between 5 and 8

    counter = 0
 
    if queue_type == "torque":
        interval = 450
        wait = False
        ncores = 1000
        script_suff = "qsub"
        a_or_w = 'a'
        background = "&"
    elif queue_type == "slurm":
        interval = 1000
	wait = False
	ncores = 1000
        script_suff = "sbatch"
        a_or_w = 'w'
        background = ""
    else:
	interval = math.ceil(8000/14.0) #this is the number of jobs that this script should kick off in total
    	wait = True
        ncores = 58

    ps = []    

    #set list_seqs according to whether or not seqfile is present.
    if seqfile == "":
        list_seqs = [ string for string in itertools.imap(''.join, itertools.product('ACDEFGHIKLMNPQRSTVWY', repeat=3)) ]
    else:
        with open(seqfile) as s:
            lines = s.readlines()
        seqs = [ l.strip() for l in lines ]
        step = int(math.ceil(len(seqs)/float(interval)))
        list_seqs = [ seqs[start:start+step] for start in xrange(0, len(seqs), step) ]

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
		    #make sure that the correct folders exist
		    for i in item:
		        try:
			    os.mkdir(OUTPATH + i[0:3])
                        except:
                            pass
		    out.writelines('%s\n' % (i) for i in item)

	    #generic command
            command = "{bin}/discrim_sim.static.linuxgccrelease -database {db} -s {inpath}/pdbs/Job_20ly104_0032.pdb -out::path::pdb {outpath}/{prefix}/ -enzdes::cstfile {inpath}/pdbs/ly104cstfile.txt -run:preserve_header @/home/arubenstein/git_repos/general_src/enzflags -out::prefix {prefix} -resfile {inpath}/resfile/rfpackpept.txt {f}".format( bin=ROSETTA_BIN, db=ROSETTA_DB, outpath=OUTPATH, inpath=INPATH, prefix=prefix, f=fragfiles )
	    
	    #if slurm style, write script and run as a batch script
            if queue_type != "bash":
                if queue_type == "slurm":
                    script_fn = OUTPATH + prefix + '/' + prefix + "." + script_suff
                elif seqfile != "": #really should have a third option for tyr not seqfile
                    job_count=int(math.ceil(counter/30.0))
                    script_fn = "{o}{c}.{suff}".format(o=OUTPATH, c=job_count, suff=script_suff)

	        with open(script_fn, a_or_w) as script:
		    if fen2 == "true":
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --job-name={p}\n#SBATCH -p main\n#SBATCH --export=ALL\n#SBATCH -o {outpath}{p}/slurm{s}.out\n#SBATCH --time=30:00:00\n".format(p = prefix,outpath=OUTPATH)
		    elif queue_type == "slurm":
		        header = "#!/bin/bash\n#SBATCH -n 1\n#SBATCH -c 1\n#SBATCH --job-name={p}\n#SBATCH -o {outpath}{p}/slurm{p}.out\n\n".format(p = prefix, outpath=OUTPATH)
                    elif queue_type == "torque": #is this true for tyr not seqfile?
			header = "#!/bin/bash\n#PBS -l nodes=1\n#PBS -l walltime=24:00:00\n#PBS -q tyr\n#PBS -N {c}\n#PBS -o {outpath}/{c}.out\n#PBS -e {outpath}/{c}.err\n".format(c = job_count, outpath=OUTPATH)
		    
		    #if queue_type is slurm or queue_type is torque and it's the first of 30 commands then write a header to the script
		    if queue_type == "slurm" or counter % 30 == 1:
                        script.write(header)
		    script.write(command + " > {outpath}{p}/{p}.log {bg}\n".format( outpath=OUTPATH, p=prefix, bg=background ))
                    if queue_type == "slurm" or counter % 30 == 0 or counter == len(list_seqs):
                        if queue_type == "torque":
			    script.write("\nwait\n")
	                p = Popen(script_suff + " " + script_fn, shell=True)

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
    parser.add_argument ('--queue_type', help="is this being run as bash, slurm, or torque job")
    parser.add_argument ('--fen2', default="false", help="is this being run on fen2. if yes, change some of sbatch headers")
    parser.add_argument ('--seq_file', default="", help="Optional, can input a sequences file - each sequence will be run on its own")
    args = parser.parse_args()

    main(args.server_num, args.queue_type, args.fen2, args.seq_file) 
