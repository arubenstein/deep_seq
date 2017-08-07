#!/usr/bin/perl

$inputfile = $ARGV[0];

open INPUTFILE, "$inputfile" or die $!;
$a = 0;
while($line = <INPUTFILE> )
{
	chomp $line;
		@data = split (',', $line);
		$ele = $data[8];
		$a = $a + $ele;
}
$a = $a/8;
print " $a\n";
close INPUTFILE;


