#!/usr/bin/perl

$input_file = $ARGV[0];
open INPUTFILE, "$input_file" or die "Cannot open $input_file for read!\n";
$chain_F_res_count = 0;
while($line = <INPUTFILE>)
{
	chomp $line;
	if($line =~ m/^ATOM/)
	{
		$chain_ID = substr($line, 21, 1);
		$atom_type = substr($line, 13, 1);
	        $atom_type_2 = substr($line, 13, 2);
		if($atom_type ne "H" && $atom_type_2 ne "NV")
		{
			print "$line\n";
		}
	}
}
close INPUTFILE;

