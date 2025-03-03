#!/bin/bash
#SBATCH --account=p32089
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --time=01:00:00
#SBATCH --mem=40G

module purge
module load mamba/24.3.0
module load git
eval "$(conda shell.bash hook)"

conda activate /projects/p32089/envs/moose

make clean
make -j 10
