#!/bin/bash

theta_angle=0

# Input file type
og_filename=FDTR_input_GibbsExcess_StepFunction
# og_filename=FDTR_input_Traditional
# og_filename=FDTR_CALIBRATION

x0_vals_num=("-30" "-25" "-20" "-17" "-15" "-14" "-13" "-11" "-12" "-10" "-9" "-8" "-7" "-6" "-5" "-4" "-3" "-2" "-1" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "17" "20" "25" "30")
# freq_vals_num=("1e6" "2e6" "4e6" "6e6" "8e6" "10e6")

# x0_vals_num=("0")
freq_vals_num=("0.01e6" "0.02e6" "0.04e6" "0.06e6" "0.08e6" "0.1e6" "0.2e6" "0.4e6" "0.6e6" "0.8e6" "1e6"  "2e6" "4e6" "6e6" "8e6" "10e6")

# Output file
output_file="../${og_filename}_out_theta_${theta_angle}.csv"

# Create header for the output file
echo "x0, freq, imag_part, real_part" > "$output_file"

for x0 in "${x0_vals_num[@]}"; do
	for freq in "${freq_vals_num[@]}"; do
	
			input_file="${og_filename}_Fourier_Steady_theta_${theta_angle}_freq_${freq}_x0_${x0}_out.csv"
			
			# Concatenate data to the output file using printf in awk, stopping at the specified line
			awk -v freq="$freq" -v x0="$x0" -F, 'NR>2{
			
					printf "%s, %s, %.30f, %.30f\n", x0, freq / 1e6, $2, $3
			
			}' "$input_file" >> "$output_file"
			
	done
done


echo "Concatenation complete. Output file: $output_file"
