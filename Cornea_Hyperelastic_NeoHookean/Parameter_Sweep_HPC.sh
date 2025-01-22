#!/bin/bash

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

# Function to check if there are any jobs in the Slurm queue
function check_squeue() {
    #squeue_output=$(squeue -t PD,R -u vtw1026 -h)  # Replace with your actual username
	
	squeue_output=$(squeue -t PD,R -u vtw1026 -h -o "%.18i %.9P %.80j %.8T %.10M %.6D %R" | grep Part1_Stretch)
	
    if [ -z "$squeue_output" ]; then
        return 0  # No jobs in the queue
    else
        return 1  # Jobs are in the queue
    fi
}

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

stretch_vals_num=("1.1")

# Calculate number of simulations'
num_freqs=${#freq_vals_num[@]}
num_stretches=${#stretch_vals_num[@]}
total_simulations=$((num_freqs * num_stretches - 1))

# Make new 3D mesh
python3 cornea_rectangle.py >> gmsh_output.txt &
wait

rm *.txt

for stretch_val_num in "${stretch_vals_num[@]}"; do
		# Create a new filename 
		new_filename="${step1_filename}_stretch_${stretch_val_num}.i"

		# Copy the original input file to the new filename
		cp "$step1_filename$extension1" "$new_filename"
		
		# Replace the stretch ratio in the MOOSE script
		sed -i "s/\(stretch_ratio\s*=\s*\)[0-9.eE+-]\+/\1$stretch_val_num/g" "$new_filename"
		
		# Save the new MOOSE script to the list of files
		echo $new_filename >> NeoHookeanDispersion_Stretch.txt
done

# Update the batch job file with the calculated number of simulations
sed -i "s/^#SBATCH --array=0-[0-9]\+/#SBATCH --array=0-$total_simulations/" Batch_MOOSE.sh

# Update the simulation list
sed -i "s|^simulation_list=.*|simulation_list=\"NeoHookeanDispersion_Stretch.txt\"|" Batch_MOOSE.sh

sbatch Batch_MOOSE.sh






part2_complete=0

while [ $part2_complete -eq 0 ]; do
	if check_squeue; then

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
				
				# Save the new MOOSE script to the list of files
				echo $new_filename_2 >> NeoHookeanDispersion_Harmonic.txt
			done
		done
	
		part2_complete=1
	else
        echo "Jobs are in the queue. Waiting..."
    fi

    # Sleep for a while before checking again (e.g., 5 minutes)
    sleep 300

done

# Update the simulation list
sed -i "s|^simulation_list=.*|simulation_list=\"NeoHookeanDispersion_Harmonic.txt\"|" Batch_MOOSE.sh

sbatch Batch_MOOSE.sh