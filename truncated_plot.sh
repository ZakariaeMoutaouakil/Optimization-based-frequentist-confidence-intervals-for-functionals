#!/bin/bash

# Activate the virtual environment
source /home/pc/Projects/optimisation/.venv/bin/activate

# Assign the arguments
limit=70
sigma=0.12

# Base directory
base_dir="/home/pc/Projects/output/cifar10/noise_${sigma}"

# Path to certification output file
certification_output_file="${base_dir}/certification_output.tsv"

# Get the number of lines in the certification output file
num_lines=$(wc -l < "$certification_output_file")

# Initialize the files and labels arrays
files=("$certification_output_file")
labels=("Cohen(100/10000)")

# Loop to construct the files and labels arrays
for (( N=20; N<=limit; N+=10 )); do
  transform_output_file="${base_dir}/N_${N}/transform_output.tsv"

  # Truncate the transform output file to match the number of lines in the certification output file
  truncated_file="${base_dir}/N_${N}/transform_output_truncated.tsv"
  head -n "$num_lines" "$transform_output_file" > "$truncated_file"

  files+=("$truncated_file")
  labels+=("Me(N=${N})")
done

# Execute the python command with constructed arguments
python -m certify.plot --files "${files[@]}" --labels "${labels[@]}" --plot /tmp/plot.png --log /tmp/log.log

# Deactivate the virtual environment
deactivate
