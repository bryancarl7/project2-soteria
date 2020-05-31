#!/bin/bash

if [ "$1" == "-run" ] ; then
  echo "---------------------------------------------------------------"
	echo "                ...Launching Flask Server..."
	echo "---------------------------------------------------------------"
  python3 -m server.api
fi

if [ "$1" == "-windows"  ] ; then
	builds/build_windows "$2"
else
  builds/build_linux "$1"
fi
