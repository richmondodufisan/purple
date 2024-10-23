#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --array=0-59
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20 ## how many cpus or processors do you need on each computer
#SBATCH --time=4:00:00 ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=1G ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name=Part1_Stretch  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --exclude=qnode0565,qnode0626,qnode0637,qnode0019,qnode0115,qnode1201

#moose_exec.sh ../purple-opt -i ${script_name} --mesh-only
#moose_exec.sh ../purple-opt -i ${script_name}

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

simulation_list="NeoHookeanDispersion_Stretch.txt"

IFS=$'\n' read -d '' -r -a lines < ${simulation_list}

mpiexec -np ${SLURM_NTASKS} singularity exec -B /projects:/projects -B /projects/p32089/moose:/opt/moose /projects/p32089/moose_latest.sif /projects/p32089/purple/purple-opt -i ${lines[$SLURM_ARRAY_TASK_ID]}