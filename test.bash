#!/usr/bin/env bash

# SPDX-License-Identifier: MIT

# Create test directory with various symlinks.


set -Ceu
set -o pipefail
shopt -s failglob
shopt -s shift_verbose


function trace() {
	local -
	set -x
	"${@}"
}


function main() {
	mkdir test
	cd test
	trace mkdir -pv  \
		links/{a,b/{c,d/e}}  \
		targets/{a,b,c,d/e}
	trace touch  \
		targets/{a/{o,p},b/q,{c/r,d/e/s}}
	ln -sv {"${PWD}"/targets,links}/a/o
	ln -sv {"${PWD}"/targets,links}/a/p
	ln -sv {"${PWD}"/targets,links}/b/q
	ln -sv  "${PWD}"/targets/c/r   links/b/c/r
	ln -sv  "${PWD}"/targets/d/e/s links/b/d/e/s
	exit  # keep to be robust against script changes during runtime
}


if ! (return 0) 2>/dev/null
then
	# execute only if not sourced
	main "${@}"
fi
