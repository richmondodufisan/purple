#!/bin/bash

# Input file type
og_filename=FDTR_Two_Layer

x0_vals_num=("0")
freq_vals_num=("1e6")

# Output file
output_file="./${og_filename}_axisymmetric_out.csv"

# Create header for the output file
echo "x0, freq, imag_part, real_part" > "$output_file"

for x0 in "${x0_vals_num[@]}"; do
	for freq in "${freq_vals_num[@]}"; do
	
			input_file="${og_filename}_out.csv"
			
			# Concatenate data to the output file using printf in awk, stopping at the specified line
			awk -v freq="$freq" -v x0="$x0" -F, 'NR>2{
			
					printf "%s, %s, %.30f, %.30f\n", x0, freq / 1e6, $2, $3
			
			}' "$input_file" >> "$output_file"
			
	done
done


echo "Concatenation complete. Output file: $output_file"
