#!/bin/bash

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

# Original file name
# og_filename="FDTR_input_GibbsExcess"
# extension=".i"

og_filename=FDTR_input_Traditional
extension=".i"

# Original file name (calibration)
# og_filename="FDTR_CALIBRATION"
# extension=".i"

og_mesh_script="FDTR_mesh"
og_mesh_ext=".py"

# Define the range of values you want to loop over

x0_vals_num=("0")

# freq_vals_num=("1e6")

theta_vals_num=("0")

#x0_vals_num=("-30" "-25" "-20" "-17" "-15" "-14" "-13" "-11" "-12" "-10" "-9" "-8" "-7" "-6" "-5" "-4" "-3" "-2" "-1" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "17" "20" "25" "30")

freq_vals_num=("1e6" "2e6" "4e6" "6e6" "8e6" "10e6")

#theta_vals_num=("0" "15" "30" "45" "60" "75")


# Loop over values
for x0_val_num in "${x0_vals_num[@]}"; do
	for theta_val_num in "${theta_vals_num[@]}"; do
	
		# Replace the x0_val value in the mesh script
		sed -i "s/\(xcen\s*=\s*\)[0-9.eE+-]\+/\1$x0_val_num/g" "${og_mesh_script}${og_mesh_ext}"
		
		# Replace the theta_val value in the mesh script
		sed -i "0,/theta\s*=\s*[0-9.eE+-]\+/{s//theta = $theta_val_num/}" "${og_mesh_script}${og_mesh_ext}"
		
		# Replace the mesh name in the mesh script
		new_mesh_name="${og_mesh_script}_x0_${x0_val_num}_theta_${theta_val_num}.msh"
		sed -i "0,/newMeshName = [^ ]*/s/newMeshName = [^ ]*/newMeshName = \"$new_mesh_name\"/" "${og_mesh_script}${og_mesh_ext}"	
		
		#echo "$new_mesh_name"
		
		# Make new 3D mesh
		#python3 FDTR_mesh.py >> gmsh_output.txt &
		#wait
		
		echo "Mesh Generated, x0 = ${x0_val_num}, theta = ${theta_val_num}"
		
		for freq_val_num in "${freq_vals_num[@]}"; do
			# Create a new filename by appending x0_val to the original filename
			new_filename="${og_filename}_Fourier_Steady_theta_${theta_val_num}_freq_${freq_val_num}_x0_${x0_val_num}.i"

			# Copy the original input file to the new filename
			cp "$og_filename$extension" "$new_filename"
			
			# Replace the theta_val value in the new input file
			sed -i "s/\(theta_deg\s*=\s*\)[0-9.eE+-]\+/\1$theta_val_num/g" "$new_filename"
			
			# Replace the freq_val value in the new input file
			sed -i "s/\(freq_val\s*=\s*\)[0-9.eE+-]\+/\1$freq_val_num/g" "$new_filename"

			# Replace the x0_val value in the new input file
			sed -i "s/\(x0_val\s*=\s*\)[0-9.eE+-]\+/\1$x0_val_num/g" "$new_filename"
			
			# Replace the mesh in the MOOSE script
			sed -i "0,/file = [^ ]*/s/file = [^ ]*/file = \"$new_mesh_name\"/" "$new_filename"
			
			# Replace the input file in the Batch script
			sed -i "0,/script_name=[^ ]*/s/script_name=[^ ]*/script_name=\"$new_filename\"/" "FDTR_Batch_MOOSE.sh"
			
			freq_noexp=$(python3 -c "import math; print(int($freq_val_num*1e-6))")
			
			# Replace the job name
			sed -E -i "s/(#SBATCH --job-name=)[^[:space:]]+/\1${x0_val_num}${freq_noexp}${theta_val_num}_Fourier_Steady_Formulation/" "FDTR_Batch_MOOSE.sh"

			# Submit job
			sbatch FDTR_Batch_MOOSE.sh
		done
	done
done
