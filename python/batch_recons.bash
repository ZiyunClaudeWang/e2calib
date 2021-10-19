#!/bin/bash
# Read a string with spaces using for loop
search_dir=$1
echo "$search_dir"
for entry in "$search_dir"/*.h5;
do
    python offline_reconstruction.py  --freq_hz 10 --upsample_rate 2 --h5file $entry --height 480 --width 640
done
