#!/bin/bash
# Read a string with spaces using for loop
search_dir=$1
echo "$search_dir"
for entry in "$search_dir"/*.raw;
do
    python3 convert.py $entry
done
