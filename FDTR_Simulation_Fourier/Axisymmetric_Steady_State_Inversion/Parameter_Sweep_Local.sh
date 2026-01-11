#!/bin/bash

# Original file name
og_filename="FDTR_input_Traditional_Axisymmetric"
extension=".i"

# Define the range of values you want to loop over

freq_vals_num=("1e6" "2e6" "4e6" "6e6" "8e6" "10e6")



# Clear the output files before appending
> SteadyStateFourier.txt
> MeshCreation.txt


# Loop over values
for freq_val_num in "${freq_vals_num[@]}"; do

	# Create a new filename by appending x0_val to the original filename
	new_filename="${og_filename}_freq_${freq_val_num}_x0_0.i"

	# Copy the original input file to the new filename
	cp "$og_filename$extension" "$new_filename"

	
	# Replace the freq_val value in the new input file
	sed -i "s/\(freq_val\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "$new_filename"
	
	# Run the job
	../../purple-opt -i ${new_filename}
	
done

