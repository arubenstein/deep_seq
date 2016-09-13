#!/bin/bash
#

inp_pdb=$1
path=$2
scripts=$3
torque=$4

full_pdb_path=$path'/'$inp_pdb'.pdb'
outpath=$path'/'$inp_pdb'/'

mkdir -p $path'/'$inp_pdb

perl $scripts'/modify2.pl' $full_pdb_path > $outpath'/'$inp_pdb'.pdb'

cd $outpath
#6.131s real
rm -rf tleap.in
cat >tleap.in <<EOF
source leaprc.gaff
source leaprc.ff12SB
loadamberparams frcmod.ionsjc_tip3p
d = loadpdb "$inp_pdb.pdb"
addions d Cl- 0
charge d
saveamberparm d $inp_pdb.prmtop $inp_pdb.inpcrd
quit
EOF
tleap -f tleap.in

if [[ $torque -eq 1 ]]
then
	script_pre=$scripts'/'
else
	script_pre=""
fi

#3.901s real
$script_pre'ante-MMPBSA.py' -p $inp_pdb.prmtop -c $inp_pdb'_c.prmtop' -s @Cl-
#5.350s real
$script_pre'ante-MMPBSA.py' -p $inp_pdb'_c.prmtop' -r $inp_pdb'_r.prmtop' -l $inp_pdb'_l.prmtop' -n :197-206


#26.889s real
$script_pre'MMPBSA.py' -O -i $scripts'/'mmpbsa.in -o $inp_pdb'_FINAL_RESULTS_MMPBSA.dat' -sp $inp_pdb.prmtop -cp $inp_pdb'_c.prmtop' -rp $inp_pdb'_r.prmtop' -lp $inp_pdb'_l.prmtop' -y *.inpcrd > progress.log 2>&1

grep " 198," FINAL_DECOMP_MMPBSA.dat > log1
grep " 199," FINAL_DECOMP_MMPBSA.dat > log2
grep " 200," FINAL_DECOMP_MMPBSA.dat > log3
grep " 201," FINAL_DECOMP_MMPBSA.dat > log4
grep " 202," FINAL_DECOMP_MMPBSA.dat > log5
grep " 203," FINAL_DECOMP_MMPBSA.dat > log6
grep " 204," FINAL_DECOMP_MMPBSA.dat > log7
grep " 205," FINAL_DECOMP_MMPBSA.dat > log8

cat log1 log2 log3 log4 log5 log6 log7 log8 > dat
awk 'NR%2==1' dat > dat_complex
awk 'NR%2==o' dat > dat_binding

perl $scripts'/'mean_complex.pl dat_complex > temp_complex 
perl $scripts'/'mean_binding.pl dat_binding > temp_binding

rm dat*
rm log*
rm _MMPBSA*
rm *.prmtop
rm *.inpcrd
rm tleap.in
rm leap.log
rm FINAL_DECOMP_MMPBSA.dat
rm progress.log
rm $inp_pdb'.pdb'

mv temp_complex '../'$inp_pdb'_dat_complex'
mv temp_binding '../'$inp_pdb'_dat_binding'

 
