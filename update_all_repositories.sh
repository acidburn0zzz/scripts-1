#!/bin/zsh

if ! [ $1 ]; then
	echo "Invalid args: required paths directories containing git repositories";
	exit;
fi;

root=$(pwd);
for i ($@) {
	for j ($i/*/) {
		if ! [ -d $j/.git/ ]; then
			echo "Git repository was not found at " $j " skipping...";
			continue;
		fi;

		cd $j;
		GitSync;
		cd $root;
	}
}
