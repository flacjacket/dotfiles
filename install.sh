#!/bin/bash
# Add all folders and symlinks all files in the ./dotfiles directory (relative
# to this script) to ~, prompting before overwrite

function clobber() {
	read -p "$1 exists, overwrite? [N/y] " response
	if [ "$response" == "y" ]; then
		return 0
	fi
	return 1
}

function add_file() {
	orig=$1
	dest=$2
	if [ -f $dest ] && $(clobber $dest) || ! [ -f $dest ]; then
		ln -svf "$orig" "$dest"
	fi
}

function add_folder() {
	orig_folder=$1
	dest_folder=$2
	[ -d $dest_folder ] || mkdir -v $dest_folder
	for i in $(find $orig_folder -mindepth 1 -maxdepth 1); do
		[ -f $i ] && add_file $i $dest_folder/$(basename $i)
		[ -d $i ] && add_folder $i $dest_folder/$(basename $i)
		orig_folder=$1 && dest_folder=$2
	done
}


dir=`dirname $PWD/$0`
add_folder $dir/dotfiles ~
