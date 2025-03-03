#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --array=0-428
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20 ## how many cpus or processors do you need on each computer
#SBATCH --time=4:00:00 ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=8G ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name=fourier  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --exclude=qnode0565

#moose_exec.sh ../purple-opt -i ${script_name} --mesh-only
#moose_exec.sh ../purple-opt -i ${script_name}

module purge
module load mamba/24.3.0
module load git
eval "$(conda shell.bash hook)"

conda activate /projects/p32089/envs/moose

IFS=$'\n' read -d '' -r -a lines < SteadyStateFourier.txt

mpirun -np ${SLURM_NTASKS} /projects/p32089/purple/purple-opt -i ${lines[$SLURM_ARRAY_TASK_ID]}
