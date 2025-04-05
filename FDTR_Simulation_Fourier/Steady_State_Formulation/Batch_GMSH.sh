#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --array=0-26
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5 ## how many CPUs or processors do you need on each computer
#SBATCH --time=1:00:00 ## how long does this need to run (different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=2G ## how much RAM per CPU
#SBATCH --job-name=mesh  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --output=mesh_x0_%a.out ## dynamically sets the output file name
#SBATCH --exclude=qnode0565


module purge
module load mamba/24.3.0
module load git
eval "$(conda shell.bash hook)"

conda activate gmsh-env


IFS=$'\n' read -d '' -r -a lines < MeshCreation.txt

python3 "${lines[$SLURM_ARRAY_TASK_ID]}"
