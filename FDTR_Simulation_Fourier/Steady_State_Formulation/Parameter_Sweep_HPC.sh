#!/bin/bash

# Original file name
og_filename="FDTR_input_GibbsExcess_StepFunction_BesselRing"
extension=".i"

og_mesh_script="FDTR_mesh"
og_mesh_ext=".py"

# Define the range of values you want to loop over

# x0_vals_num=("0")

# freq_vals_num=("1e6"  "1.2e6"  "1.4e6"  "1.6e6"  "1.8e6")

theta_vals_num=("0")

x0_vals_num=("-30" "-25" "-20" "-17" "-15" "-14" "-13" "-11" "-12" "-10" "-9" "-8" "-7" "-6" "-5" "-4" "-3" "-2" "-1" "0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "17" "20" "25" "30")

freq_vals_num=("1e6"  "2e6" "4e6" "6e6" "8e6" "10e6" "20e6" "40e6" "60e6" "80e6" "100e6")

# theta_vals_num=("40" "45" "50" "55" "60" "65" "70" "75" "80" "85")


# Clear the output file before appending
> SteadyStateFourier.txt


# Loop over values
for x0_val_num in "${x0_vals_num[@]}"; do

	# Replace the x0_val value in the mesh script
	sed -i "s/\(xcen\s*=\s*\)[0-9.eE+-]\+/\1$x0_val_num/g" "${og_mesh_script}${og_mesh_ext}"
	
	# Replace the mesh name in the mesh script
	new_mesh_name="${og_mesh_script}_x0_${x0_val_num}.msh"
	sed -i "0,/newMeshName = [^ ]*/s/newMeshName = [^ ]*/newMeshName = \"$new_mesh_name\"/" "${og_mesh_script}${og_mesh_ext}"	
	
	#echo "$new_mesh_name"
	
	# Make new 3D mesh
	python3 FDTR_mesh.py >> gmsh_output.txt &
	wait

	echo "Mesh Generated, x0 = ${x0_val_num}"

	for theta_val_num in "${theta_vals_num[@]}"; do
		
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
			
			# Save the new MOOSE script to the list of files
			echo $new_filename >> SteadyStateFourier.txt
		done
	done
done


# Count the number of lines in SteadyStateFourier.txt
num_jobs=$(wc -l < SteadyStateFourier.txt)

# Update the job array in the SLURM script using sed
if [ "$num_jobs" -gt 0 ]; then
    sed -i "s/^#SBATCH --array=[0-9-]*/#SBATCH --array=0-$((num_jobs-1))/" FDTR_Batch_MOOSE.sh
    echo "Updated job array to 0-$((num_jobs-1)) in FDTR_Batch_MOOSE.sh"
else
    echo "Error: No jobs found in SteadyStateFourier.txt"
    exit 1
fi