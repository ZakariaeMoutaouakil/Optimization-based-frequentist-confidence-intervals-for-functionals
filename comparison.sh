#!/bin/bash

# Activate the virtual environment
source "$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals/venv/bin/activate"

# Set locale to ensure decimal point handling
export LC_NUMERIC="C"
export PYTHONPATH="$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals"

for sigma in 0.12 0.25 0.50 1.00
do
    sigma_str=$(printf "%.2f" "$sigma")
    base_classifier_path="$HOME/models/cifar10/resnet110/noise_$sigma_str/checkpoint.pth.tar"

    for N in $(seq 20 10 100)
    do
        outfile_path="$HOME/output/cifar10/noise_$sigma_str/N_$N/certification_output.tsv"
        log_path="$HOME/output/cifar10/noise_$sigma_str/N_$N/log.log"

        # Create necessary directories
        mkdir -p "$(dirname "$outfile_path")"
        mkdir -p "$(dirname "$log_path")"

        command="python cohen/certify.py --dataset cifar10 \
        --base_classifier \"$base_classifier_path\" \
        --sigma \"$sigma_str\" \
        --N0 1 \
        --N \"$N\" \
        --outfile \"$outfile_path\" \
        --log \"$log_path\""

        echo "$command"
        eval "$command"
    done
done

# Deactivate the virtual environment
deactivate
