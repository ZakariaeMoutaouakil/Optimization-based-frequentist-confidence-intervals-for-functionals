#!/bin/bash

# Activate the virtual environment
source "$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals/venv/bin/activate"

# Set locale to ensure decimal point handling
export LC_NUMERIC="C"
export PYTHONPATH="$HOME/Optimization-based-frequentist-confidence-intervals-for-functionals"

# Loop over sigma values
for sigma in 0.12 0.25 0.50 1.00
do
    sigma_str=$(printf "%.2f" "$sigma")

    # Loop over N values
    for N in $(seq 20 10 100)
    do
        infile_path="$HOME/output/cifar10/noise_$sigma_str/N_$N/certification_output.tsv"
        outfile_path="$HOME/output/cifar10/noise_$sigma_str/N_$N/transform_output.tsv"
        log_path="$HOME/output/cifar10/noise_$sigma_str/N_$N/transform_log.log"

        # Check if the input file exists
        if [ -f "$infile_path" ]; then
            if [ -f "$outfile_path" ]; then
                echo "Output file $outfile_path already exists. Skipping..."
            else
                # Create necessary directories
                mkdir -p "$(dirname "$outfile_path")"
                mkdir -p "$(dirname "$log_path")"

                # Run the transformation command
                command="python main_basic.py --data \"$infile_path\" \
                --outfile \"$outfile_path\" \
                --sigma \"$sigma_str\" \
                --log \"$log_path\""

                echo "$command"
                eval "$command"
            fi
        else
            echo "Input file $infile_path does not exist. Skipping..."
        fi
    done
done

# Deactivate the virtual environment
deactivate
