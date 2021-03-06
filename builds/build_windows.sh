#!/bin/bash
export FLASK_APP=server.py
export FLASK_ENV=development

# Database connection must be tested everytime regardless of skip flag
first_install=1
log_skip=1

# You can specify the -skip flag at runtime to skip over trying to install requirements
if [ "$1" == "-skip" ] ; then
	python=1
	req=1
else
	python=0
	req=0
	mkdir tmp/
	touch tmp/soteria.log
fi

# Checks for correct python version
if [[ python == 0 ]] ; then
  version=$(py -V 2>&1 | grep -Po '(?<=Python )(.+)')
  if [[ -z "$version" ]] ; then
    echo "Requires Python 3.7.5 or higher to run"
    exit 1;
  else
    python=1
  fi
fi

# Pip installs any python package required from "requirements.txt"
if [ "$req" != 1 ] ; then
 	while read p; do
	 py -m pip install $p --user
 	done < requirements.txt
	req=1
fi

# Try to kickstart Python Server:
py -m server.api
