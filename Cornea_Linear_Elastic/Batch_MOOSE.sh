#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10 ## how many cpus or processors do you need on each computer
#SBATCH --time=0:10:00 ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=100M ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name=1.1_0_Cornea_Harmonic  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --exclude=qnode0565,qnode0626,qnode0637,qnode0019,qnode0115


script_name="FDTR_input_GibbsExcess_Fourier_Steady_theta_45_freq_2e6_x0_-3.i"

#moose_exec.sh ../purple-opt -i ${script_name} --mesh-only
#moose_exec.sh ../purple-opt -i ${script_name}

mpiexec -np ${SLURM_NTASKS} singularity exec -B /projects:/projects -B /scratch:/scratch -B /projects/p32089/singularity/moose/moose:/opt/moose /projects/p32089/singularity/moose_latest.sif /projects/p32089/MOOSE_Applications/purple/purple-opt -i ${script_name}
