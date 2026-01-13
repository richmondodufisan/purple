#!/bin/bash

# Input file type
og_filename="FDTR_input_Traditional_Axisymmetric"

x0_vals_num=("0")
freq_vals_num=("1e6" "2e6" "3e6" "4e6" "6e6" "8e6" "10e6")

# Output file
output_file="../${og_filename}_5_00_um.csv"

# Create header for the output file
echo "x0, freq, imag_part, real_part" > "$output_file"

for x0 in "${x0_vals_num[@]}"; do
    for freq in "${freq_vals_num[@]}"; do

        input_file="${og_filename}_freq_${freq}_x0_${x0}_out.csv"

        # Check if file exists
        if [[ ! -f "$input_file" ]]; then
            echo "Warning: Missing file $input_file"
            continue
        fi

        # Check if the 3rd line is empty
        third_line=$(sed -n '3p' "$input_file" | tr -d '[:space:]')
        
        if [[ -z "$third_line" ]]; then
            echo "Warning: Missing data at frequency=${freq}Hz and x0=${x0}. File: $input_file"
            continue
        fi

        # Concatenate data to the output file using printf in awk, stopping at the specified line
        awk -v freq="$freq" -v x0="$x0" -F, 'NR>2{
                printf "%s, %s, %.30f, %.30f\n", x0, freq / 1e6, $2, $3
        }' "$input_file" >> "$output_file"

    done
done

echo "Concatenation complete. Output file: $output_file"
