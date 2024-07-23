#!/bin/bash

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

# Function to check if there are any jobs in the Slurm queue
function check_squeue() {
    #squeue_output=$(squeue -t PD,R -u vtw1026 -h)  # Replace with your actual username
	
	squeue_output=$(squeue -t PD,R -u vtw1026 -h -o "%.18i %.9P %.80j %.8T %.10M %.6D %R" | grep Cornea_Stretch)
	
    if [ -z "$squeue_output" ]; then
        return 0  # No jobs in the queue
    else
        return 1  # Jobs are in the queue
    fi
}

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
		
		
		
		
		# Replace the input file in the Batch script
		sed -i "0,/script_name=[^ ]*/s/script_name=[^ ]*/script_name=\"$new_filename\"/" "Batch_MOOSE.sh"
		
		freq_noexp=$(python3 -c "import math; print(int($freq_val_num*1e-6))")
		
		# Replace the job name
		sed -E -i "s/(#SBATCH --job-name=)[^[:space:]]+/\1${stretch_val_num}_${freq_noexp}_Cornea_Stretch/" "Batch_MOOSE.sh"
		
		# Submit job
		sbatch Batch_MOOSE.sh
			
	done
done


part2_complete=0

while [ $part2_complete -eq 0 ]; do
	if check_squeue; then

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
				
				
				
				
				
				# Replace the input file in the Batch script
				sed -i "0,/script_name=[^ ]*/s/script_name=[^ ]*/script_name=\"$new_filename_2\"/" "Batch_MOOSE.sh"
				
				freq_noexp=$(python3 -c "import math; print(int($freq_val_num*1e-6))")
				
				# Replace the job name
				sed -E -i "s/(#SBATCH --job-name=)[^[:space:]]+/\1${stretch_val_num}_${freq_noexp}_Cornea_Harmonic/" "Batch_MOOSE.sh"
				
				# Submit job
				sbatch Batch_MOOSE.sh
			done
		done
	
		part2_complete=1
	else
        echo "Jobs are in the queue. Waiting..."
    fi

    # Sleep for a while before checking again (e.g., 5 minutes)
    sleep 300

done
