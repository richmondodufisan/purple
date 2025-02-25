#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --array=0-4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=21 ## how many cpus or processors do you need on each computer
#SBATCH --time=4:00:00 ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=4G ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name=301085_Fourier_Steady_Formulation_test_rcs_support  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --exclude=qnode0565,qnode0626,qnode0637,qnode0019,qnode0115,qnode1201

#moose_exec.sh ../purple-opt -i ${script_name} --mesh-only
#moose_exec.sh ../purple-opt -i ${script_name}

module purge
module use /software/spack_v20d1/spack/share/spack/modules/linux-rhel7-x86_64/
module load singularity
module load mpi/mpich-4.0.2-gcc-10.4.0

IFS=$'\n' read -d '' -r -a lines < SteadyStateFourier.txt

mpiexec -np ${SLURM_NTASKS} singularity exec -B /projects:/projects -B /scratch:/scratch -B /projects/p32089/moose:/opt/moose /projects/p32089/moose-dev_e930b1d.sif /projects/p32089/MOOSE_Applications/purple/purple-opt -i ${lines[$SLURM_ARRAY_TASK_ID]}


