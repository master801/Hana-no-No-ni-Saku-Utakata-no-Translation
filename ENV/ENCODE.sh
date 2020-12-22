#!/bin/sh

rm -rf "MODIFIED/patch2"
mkdir "MODIFIED/patch2"

cd Hana-no-No-ni-Saku-Utakata-no-Translation
python3 ./export.py
cd ..

cp --verbose -RL -t "MODIFIED/patch2" "WORKING/patch2/scn" "WORKING/patch2/image" "WORKING/patch2/uipsd"

python3 ./ENCODE.py --process_scn
