#!/bin/bash

# Step 1, Stretch
step1_filename="Part1_Stretch"
extension1=".i"

# Step 2, Harmonic Perturbation
step2_filename="Part2_Harmonic"
extension2=".i"

# Mesh Script
og_mesh_script="cornea_rectangle"
og_mesh_ext=".py"


# Define the range of values you want to loop over
freq_vals_num=("1e3" "10e3")
stretch_vals_num=("1.1" "1.2")  # Added a second stretch value for testing

# Make new 3D mesh
python3 cornea_rectangle.py &
wait

for stretch_val_num in "${stretch_vals_num[@]}"; do
		# Create a new filename 
		new_filename="${step1_filename}_stretch_${stretch_val_num}.i"

		# Copy the original input file to the new filename
		cp "$step1_filename$extension1" "$new_filename"
		
		# Replace the stretch ratio in the MOOSE script
		sed -i "s/\(stretch_ratio\s*=\s*\)[0-9.eE+-]\+/\1$stretch_val_num/g" "$new_filename"
		
		# ../purple-opt -i ${new_filename}
done


for stretch_val_num in "${stretch_vals_num[@]}"; do
	for freq_val_num in "${freq_vals_num[@]}"; do

		# Create a new filename 
		new_filename_2="${step2_filename}_freq_${freq_val_num}_stretch_${stretch_val_num}.i"
		mesh_filename_2="${step1_filename}_stretch_${stretch_val_num}_out.e"
		
		# Copy the original input file to the new filename
		cp "$step2_filename$extension2" "$new_filename_2"
		
		# Replace the mesh in the MOOSE script
		sed -i "0,/file = [^ ]*/s/file = [^ ]*/file = \"$mesh_filename_2\"/" "$new_filename_2"
		
		# Replace the frequency in the MOOSE script
		sed -i "s/\(freq_val\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "$new_filename_2"
		
		../purple-opt -i ${new_filename_2}
	done
done