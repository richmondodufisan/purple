#!/bin/bash

# Step 1, Stretch
step1_filename="Cornea_Stretch"
extension1=".i"

# Step 2, Harmonic Perturbation
step2_filename="Cornea_Harmonic_Perturbation_Steady"
extension2=".i"

# Mesh Script
og_mesh_script="cornea_rectangle"
og_mesh_ext=".py"


# Define the range of values you want to loop over
freq_vals_num=("1e3" "10e3")

stretch_vals_num=("1.1")


for stretch_val_num in "${stretch_vals_num[@]}"; do
	for freq_val_num in "${freq_vals_num[@]}"; do

		# Replace the frequency value in the mesh script
		sed -i "s/\(freq\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "${og_mesh_script}${og_mesh_ext}"
		
		# Replace the mesh name in the mesh script
		new_mesh_name="${og_mesh_script}_freq_${freq_val_num}.msh"
		sed -i "0,/newMeshName = [^ ]*/s/newMeshName = [^ ]*/newMeshName = \"$new_mesh_name\"/" "${og_mesh_script}${og_mesh_ext}"	
		
		# Make new 3D mesh
		python3 cornea_rectangle.py >> gmsh_output.txt &
		wait


		# Calculate the new length of the plate
		plate_length=$(python3 -c "import math; print(0.2 / ($freq_val_num / 1e3))")

		# Create a new filename 
		new_filename="${step1_filename}_freq_${freq_val_num}_stretch_${stretch_val_num}.i"

		# Copy the original input file to the new filename
		cp "$step1_filename$extension1" "$new_filename"
		
		# Replace the mesh in the MOOSE script
		sed -i "0,/file = [^ ]*/s/file = [^ ]*/file = \"$new_mesh_name\"/" "$new_filename"
		
		# Replace the plate length in the MOOSE script
		sed -i "s/\(l_plate\s*=\s*\)[0-9.eE+-]\+/\1$plate_length/g" "$new_filename"
		
		# Replace the stretch ratio in the MOOSE script
		sed -i "s/\(stretch_ratio\s*=\s*\)[0-9.eE+-]\+/\1$stretch_val_num/g" "$new_filename"
		
		# Run the new input file
		# ../purple-opt -i ${new_filename} &
		# wait
			
	done
done



for stretch_val_num in "${stretch_vals_num[@]}"; do
	for freq_val_num in "${freq_vals_num[@]}"; do

		# Create a new filename 
		new_filename_2="${step2_filename}_freq_${freq_val_num}_stretch_${stretch_val_num}.i"
		mesh_filename_2="${step1_filename}_freq_${freq_val_num}_stretch_${stretch_val_num}_out.e"
		
		# Copy the original input file to the new filename
		cp "$step2_filename$extension2" "$new_filename_2"
		
		# Replace the mesh in the MOOSE script
		sed -i "0,/file = [^ ]*/s/file = [^ ]*/file = \"$mesh_filename_2\"/" "$new_filename_2"
		
		# Replace the frequency in the MOOSE script
		sed -i "s/\(freq_val\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "$new_filename_2"
		
		# Run the new input file
		../purple-opt -i ${new_filename_2} &
		wait
	done
done