#!/bin/bash

# Activate the virtual environment
source /home/pc/Projects/optimisation/.venv/bin/activate

# Assign the arguments
limit=70
sigma=0.12

# Initialize the files and labels arrays
files=("/home/pc/Projects/output/cifar10/noise_${sigma}/certification_output.tsv")
labels=("Cohen(100/10000)")

# Loop to construct the files and labels arrays
for (( N=20; N<=limit; N+=10 )); do
  files+=("/home/pc/Projects/output/cifar10/noise_${sigma}/N_${N}/transform_output.tsv")
  labels+=("Me(N=${N})")
done

# Execute the python command with constructed arguments
python -m certify.plot --files "${files[@]}" --labels "${labels[@]}" --plot /tmp/plot.png --log /tmp/log.log

# Deactivate the virtual environment
deactivate
