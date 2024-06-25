#!/bin/bash

# Activate the virtual environment
source "$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals/venv/bin/activate"

# Set locale to ensure decimal point handling
export LC_NUMERIC="C"
export PYTHONPATH="$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals"
export IMAGENET_DIR="$HOME/imagenet"

for sigma in 0.25 0.50 1.00
do
    sigma_str=$(printf "%.2f" "$sigma")
    base_classifier_path="$HOME/models/imagenet/resnet50/noise_$sigma_str/checkpoint.pth.tar"
    outfile_path="$HOME/output/imagenet/noise_$sigma_str/certification_output.tsv"
    log_path="$HOME/output/imagenet/noise_$sigma_str/log.log"

    # Create necessary directories
    mkdir -p "$(dirname "$outfile_path")"
    mkdir -p "$(dirname "$log_path")"

    command="python cohen/certify.py --dataset imagenet \
    --base_classifier \"$base_classifier_path\" \
    --sigma \"$sigma_str\" \
    --N 1000 \
    --outfile \"$outfile_path\" \
    --log \"$log_path\""

    echo "$command"
    eval "$command"
done

# Deactivate the virtual environment
deactivate
