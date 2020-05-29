#!/bin/bash

if [ "$1" == "-windows"  ] ; then
	build/build_windows "$2"
else
  build/build_linux "$1"
fi