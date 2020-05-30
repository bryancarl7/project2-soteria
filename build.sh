#!/bin/bash

if [ "$1" == "-windows"  ] ; then
	builds/build_windows "$2"
else
  builds/build_linux "$1"
fi
