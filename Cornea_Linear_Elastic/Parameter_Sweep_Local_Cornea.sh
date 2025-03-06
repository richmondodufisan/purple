#!/bin/bash

# Simulation File
filename="Cornea_Harmonic_Perturbation_2D_Axisymmetric"
extension1=".i"

# Define the range of values you want to loop over
freq_vals_num=("1e3" "1.5e3" "2e3" "2.5e3" "3e3" "3.5e3" "4e3" "4.5e3" "5e3" "5.5e3" "6e3" "6.5e3" "7e3" "7.5e3" "8e3" "8.5e3" "9e3" "9.5e3" "10e3" "10.5e3" "11e3" "11.5e3" "12e3" "12.5e3" "13e3" "13.5e3" "14e3" "14.5e3" "15e3" "15.5e3" "16e3" "16.5e3" "17e3" "17.5e3" "18e3" "18.5e3" "19e3" "19.5e3" "20e3")

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