#!/bin/bash

# Simulation File
filename="Cornea_Harmonic_Perturbation_2D"
extension1=".i"

# Define the range of values you want to loop over
freq_vals_num=("100e3" "4900e3")

# Calculate number of simulations'
num_freqs=${#freq_vals_num[@]}
total_simulations=$((num_freqs - 1))

rm *.txt

for freq_val_num in "${freq_vals_num[@]}"; do
		# Create a new filename 
		new_filename="${filename}_freq_${freq_val_num}.i"

		# Copy the original input file to the new filename
		cp "$filename$extension1" "$new_filename"
		
		# Replace the frequency in the MOOSE script
		sed -i "s/\(freq_val\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "$new_filename"
		
		../purple-opt -i $new_filename
done