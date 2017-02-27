from pymol import cmd, stored

def mutate_peptide( new_seq ):
    '''
    mutate peptide to new_seq starting at second residue in the peptide
    '''

    cmd.copy(new_seq, "peptide_template")

    aa1 = list("ACDEFGHIKLMNPQRSTVWY")
    aa3 = "ALA CYS ASP GLU PHE GLY HIS ILE LYS LEU MET ASN PRO GLN ARG SER THR VAL TRP TYR".split()
    aa123 = dict(zip(aa1,aa3))

    for ind, aa in enumerate(new_seq,2):
	
        cmd.wizard("mutagenesis")
        cmd.do("refresh_wizard")
	print ind
	print aa
        # lets mutate residue 104 to GLN
        cmd.get_wizard().set_mode(aa123[aa])
        cmd.get_wizard().do_select("/{0}//B/{1}".format(new_seq, ind))
        # Select the rotamer
        #cmd.frame(1)

        # Apply the mutation
        cmd.get_wizard().apply()
        
cmd.extend( "mutate_peptide", mutate_peptide);
