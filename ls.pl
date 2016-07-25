#!/usr/bin/perl -w

####################################################################################
#This is a script, providing colored dump of directory,
# given by the arguments, or of no such, your current...
#
# This script depends on Perl.
#
# ls.pl
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
####################################################################################

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
