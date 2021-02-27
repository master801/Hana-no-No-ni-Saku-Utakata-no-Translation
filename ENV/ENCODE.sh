#!/bin/sh

#Used to copy working files to the modified folder to use later when packing the xp3 file
#Created by Master801
#Encodes translation scripts and copies game files to prepare for repacking

#Moved batch script to pure Python because Windows can't handle it...
python3 ./ENCODE.py --compile --process_scn