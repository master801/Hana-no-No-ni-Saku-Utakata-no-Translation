#!/bin/sh

rm -rf "WORKING/patch2/image" "WORKING/patch2/uipsd"
cp -r "ORIGINAL/patch2/image" "WORKING/patch2/image"
cp -r "ORIGINAL/patch2/uipsd" "WORKING/patch2/uipsd"

python3 ./DECODE.py
