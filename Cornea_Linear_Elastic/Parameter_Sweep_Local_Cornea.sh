#!/bin/bash

# Simulation File
filename="Cornea_Harmonic_Perturbation_2D_Axisymmetric"
extension1=".i"

# Define the range of values you want to loop over
freq_vals_num=("1e6" "1.5e6" "2e6" "2.5e6" "3e6" "3.5e6" "4e6" "4.5e6" "5e6" "5.5e6" "6e6" "6.5e6" "7e6" "7.5e6" "8e6" "8.5e6" "9e6" "9.5e6" "10e6" "10.5e6" "11e6" "11.5e6" "12e6" "12.5e6" "13e6" "13.5e6" "14e6" "14.5e6" "15e6" "15.5e6" "16e6" "16.5e6" "17e6" "17.5e6" "18e6" "18.5e6" "19e6" "19.5e6" "20e6")

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
		wait
done