#!/bin/bash

file_path="seeds.txt"

while IFS= read -r seed
do
    export seed=$seed; ./create_single_sample.sh
done < "$file_path"

