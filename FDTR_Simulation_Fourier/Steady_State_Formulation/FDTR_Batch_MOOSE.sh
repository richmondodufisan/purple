#!/bin/bash
#SBATCH --account=p32089  ## YOUR ACCOUNT pXXXX or bXXXX
#SBATCH --partition=short  ### PARTITION (buyin, short, normal, etc)
#SBATCH --array=0-202
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=30 ## how many cpus or processors do you need on each computer
#SBATCH --time=4:00:00 ## how long does this need to run (remember different partitions have restrictions on this param)
#SBATCH --mem-per-cpu=8G ## how much RAM do you need per CPU (this effects your FairShare score so be careful to not ask for more than you need))
#SBATCH --job-name=fourier  ## When you run squeue -u NETID this is how you can identify the job
#SBATCH --exclude=qnode0565

module purge
module load git
module load gcc/12.3.0-gcc
module load llvm/12.0.1-gcc-12.3.0
module load python/3.9.16-gcc-12.3.0
module load cmake/3.26.3-gcc-12.3.0
module load mpi/openmpi-4.1.6rc2-gcc-12.3.0
module load hdf5/1.14.1-2-gcc-12.3.0
module load gmake/4.4.1-gcc-12.3.0
module load flex/2.6.3-gcc-12.3.0
module load bison/3.8.2-gcc-12.3.0

export CC=mpicc CXX=mpicxx FC=mpif90 F90=mpif90 F77=mpif77

export HDF5_DIR=/hpc/software/spack_v20d1/spack/opt/spack/linux-rhel7-x86_64/gcc-12.3.0/hdf5-1.14.1-2-w5cjk4urzmrsa32md2hxgkc44dshuncf

export FLEX_DIR=/hpc/software/spack_v20d1/spack/opt/spack/linux-rhel7-x86_64/gcc-12.3.0/flex-2.6.3-agkmkc2za7ufjrcsi2vvp5af2t3tno7v


IFS=$'\n' read -d '' -r -a lines < SteadyStateFourier.txt

mpirun -np ${SLURM_NTASKS} /projects/p32089/moose_projects/purple/purple-opt -i ${lines[$SLURM_ARRAY_TASK_ID]}

# Get the input filename from the array
input_file="${lines[$SLURM_ARRAY_TASK_ID]}"

# Remove the .i extension to get the base name
base="${input_file%.i}"

# Build the output folder name by appending _out_cp
output_folder="${base}_out_cp"

# Remove the folder and its contents
rm -rf "${output_folder}"

