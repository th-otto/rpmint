#!/usr/bin/perl -w

use strict;
use Data::Dumper;

my $filename;


sub process_file()
{
	my $line;
	my %map;
	my $nextlabel;
	my $label;
	my $pattern;
	my $re;

	if ( ! defined(open(FILE, $filename)) ) {
		die "couldn't open $filename: $!\n";
	}
	%map = ();
	$nextlabel = 1;
	while ($line = <FILE>) {
		chomp($line);
		$line =~ s/\n//g;
		if ($line =~ /^.L([0-9]+):/ ) {
			$label = $1;
			$map{$label} = $nextlabel;
			++$nextlabel;
		}
	}	
	close(FILE);

	if ( ! defined(open(FILE, $filename)) ) {
		die "couldn't open $filename: $!\n";
	}
	if ( ! defined(open(OUT, ">$filename.new")) ) {
		die "couldn't create $filename.new: $!\n";
	}
	while ($line = <FILE>) {
		chomp($line);
		$line =~ s/\n//g;
		if ($line =~ /.L([0-9]+)/ ) {
			$label = $1;
			if (defined($map{$label})) {
				$line =~ s/.L([0-9]+)/.L$map{$label}/;
			}
		}
		print OUT "$line\n";
	}	
	close(FILE);
	close(OUT);
	rename "$filename.new", "$filename";
}

while ($filename = shift @ARGV)
{
	process_file();
}
