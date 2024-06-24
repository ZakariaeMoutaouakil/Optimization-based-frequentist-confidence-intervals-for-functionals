#!/bin/bash

# Set locale to ensure decimal point handling
export LC_NUMERIC="C"

for sigma in 0.12 0.25 0.50 1.00
do
    sigma_str=$(printf "%.2f" "$sigma")
    base_classifier_path="$HOME/models/cifar10/resnet110/noise_$sigma_str/checkpoint.pth.tar"
    outfile_path="$HOME/output/cifar10/noise_$sigma_str/certification_output.tsv"
    log_path="$HOME/output/cifar10/noise_$sigma_str/log.log"

    command="python cohen/certify.py --dataset cifar10 \
    --base_classifier \"$base_classifier_path\" \
    --sigma \"$sigma_str\" \
    --outfile \"$outfile_path\" \
    --log \"$log_path\""

    echo "$command"
    eval "$command"
done
