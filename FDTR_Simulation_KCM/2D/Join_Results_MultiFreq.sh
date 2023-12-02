#!/bin/bash

n_iterations=1

theta_angle=0

#x0_vals_num=("-15" "-10" "-9" "-8" "-7" "-6" "-5" "-4" "-3" "-2" "-1" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "15")
#freq_vals_num=("1e6" "2e6" "4e6" "6e6" "10e6")

x0_vals_num=("0")
freq_vals_num=("2e6" "3e6" "4e6" "5e6" "6e6" "7e6" "8e6" "9e6" "10e6")




for freq in "${freq_vals_num[@]}"; do

	# Output file
	output_file="../KCM_Mixed_Medium_${freq}.csv"

	# Create header for the output file
	echo "x0, freq, time, delta_temp" > "$output_file"

	for x0 in "${x0_vals_num[@]}"; do
	
		current_iteration=1
		while [ $current_iteration -le $n_iterations ]; do
			input_file="FDTR_input_KCM_Mixed_theta_${theta_angle}_freq_${freq}_x0_${x0}_v${current_iteration}_out.csv"
			
			# Concatenate data to the output file using printf in awk, stopping at the specified line
			awk -v freq="$freq" -v x0="$x0" -F, 'NR>2{
				
				printf "%s, %s, %.20f, %.20f\n", x0, freq / 1e6, $1 * 1e6, $3
			
			}' "$input_file" >> "$output_file"
			
			current_iteration=$((current_iteration + 1))

			echo "Concatenation complete. Output file: $output_file"
		done
	done
done
