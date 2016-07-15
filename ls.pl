#!/usr/bin/perl -w

use strict;
use Term::ANSIColor qw(:constants);

$Term::ANSIColor::AUTORESET = 1;

my $dir = shift @ARGV || '.';

sub printfile {
	my $fd = $_[0];

	if (-d "$dir/$fd") {
		print YELLOW "$fd\n";
	} elsif (-l "$dir/$fd") {
		print CYAN "$fd\n";
	} elsif (-x "$dir/$fd") {
		print GREEN "$fd\n";
	} elsif (-f "$dir/$fd" and -T "$dir/$fd") {
		print "$fd\n";
	} else {
		print RED "$fd\n"
	}
}

opendir DIR, $dir or die "Can't open dir $!\n";
while (my $file = readdir DIR) {
	&printfile($file);
}
