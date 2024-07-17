#!/bin/bash

# Activate the virtual environment
source "$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals/venv/bin/activate"

# Set locale to ensure decimal point handling
export LC_NUMERIC="C"
export PYTHONPATH="$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals"

sigma=0.12
sigma_str=$(printf "%.2f" "$sigma")
base_classifier_path="$HOME/models/cifar10/resnet110/noise_$sigma_str/checkpoint.pth.tar"

for N in $(seq 20 10 1000)
do
    outfile_path="$HOME/test_results/cifar10/noise_$sigma_str/N_$N/certification_output.tsv"
    log_path="$HOME/test_results/cifar10/noise_$sigma_str/N_$N/log.log"

    # Create necessary directories
    mkdir -p "$(dirname "$outfile_path")"
    mkdir -p "$(dirname "$log_path")"

    command="python cohen/certify.py --dataset cifar10 \
    --base_classifier \"$base_classifier_path\" \
    --sigma \"$sigma_str\" \
    --N0 \"$N\"  \
    --N \"$N\" \
    --max 1000 \
    --outfile \"$outfile_path\" \
    --log \"$log_path\""

    echo "$command"
    eval "$command"
done

# Deactivate the virtual environment
deactivate
