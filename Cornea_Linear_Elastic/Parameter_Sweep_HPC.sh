#!/bin/bash

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

# Step 1, Stretch
step1_filename="Cornea_Stretch"
extension=".i"

# Step 2, Harmonic Perturbation
step2_filename="Cornea_Harmonic_Perturbation_Steady"
extension=".i"

# Mesh Script
og_mesh_script="cornea_rectangle"
og_mesh_ext=".py"


# Define the range of values you want to loop over
freq_vals_num=("1e6")


for freq_val_num in "${freq_vals_num[@]}"; do


	# Replace the frequency value in the mesh script
	sed -i "s/\(freq\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "${og_mesh_script}${og_mesh_ext}"
	
	# Replace the mesh name in the mesh script
	new_mesh_name="${og_mesh_script}_freq_${freq_val_num}.msh"
	sed -i "0,/newMeshName = [^ ]*/s/newMeshName = [^ ]*/newMeshName = \"$new_mesh_name\"/" "${og_mesh_script}${og_mesh_ext}"	
	
	# Make new 3D mesh
	python3 cornea_rectangle.py >> gmsh_output.txt &
	wait


	# Create a new filename by appending x0_val to the original filename
	new_filename="${step1_filename}_Cornea_Stretch_freq_${freq_val_num}.i"

	# Copy the original input file to the new filename
	cp "$step1_filename$extension" "$new_filename"
	
	# Replace the mesh in the MOOSE script
	sed -i "0,/file = [^ ]*/s/file = [^ ]*/file = \"$new_mesh_name\"/" "$new_filename"
	
	# Replace the input file in the Batch script
	sed -i "0,/script_name=[^ ]*/s/script_name=[^ ]*/script_name=\"$new_filename\"/" "Batch_MOOSE.sh"
	
	freq_noexp=$(python3 -c "import math; print(int($freq_val_num*1e-6))")
	
	# Replace the job name
	sed -E -i "s/(#SBATCH --job-name=)[^[:space:]]+/\1${freq_noexp}_Cornea_Stretch/" "Batch_MOOSE.sh"

	# Submit job
	sbatch Batch_MOOSE.sh
done
