#!/bin/bash

n_iterations=1

theta_angle=0
# n_periods_per_iteration=2.0

# dphase=0.2

#n_timesteps=$(python3 -c "import math; print(round((1.1*$n_periods_per_iteration)/((3.5*$dphase)/360)))")

#stop_line_number=$(python3 -c "import math; print($n_timesteps+1)")

#echo $stop_line_number

# Output file
output_file="../Fourier_Mixed_Coarse_1e6.csv"

# Create header for the output file
echo "x0, freq, time, delta_temp" > "$output_file"

# Get a list of files that fit the pattern using ls -d
# file_list=$(ls -d fdtr_input_freq_*_x0_*.csv)

#x0_vals_num=("-15" "-10" "-9" "-8" "-7" "-6" "-5" "-4" "-3" "-2" "-1" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "15")
#freq_vals_num=("1e6" "2e6" "4e6" "6e6" "10e6")

x0_vals_num=("-15")
freq_vals_num=("1e6")




for x0 in "${x0_vals_num[@]}"; do
	for freq in "${freq_vals_num[@]}"; do
	
		current_iteration=1
		while [ $current_iteration -le $n_iterations ]; do
			input_file="FDTR_input_theta_${theta_angle}_freq_${freq}_x0_${x0}_v${current_iteration}_out.csv"
			
			# Concatenate data to the output file using printf in awk, stopping at the specified line
			awk -v freq="$freq" -v x0="$x0" -F, 'NR>2{
				
				printf "%s, %s, %.20f, %.20f\n", x0, freq / 1e6, $1 * 1e6, $3
			
			}' "$input_file" >> "$output_file"
			
			current_iteration=$((current_iteration + 1))
		done
	done
done


echo "Concatenation complete. Output file: $output_file"
