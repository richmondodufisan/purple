# Alternate GCC 12
source /opt/rh/gcc-toolset-12/enable

export MOOSE_DIR=/opt/moose

#
# Begin environment for moose-mpi-x86_64:765e804
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="mpi"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-mpi-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-mpi-x86_64:765e804"
export MOOSE_APPTAINER_GENERATOR_TAG="765e804"
export MOOSE_APPTAINER_GENERATOR_VERSION="765e804"

# Fix locale warnings
export LC_ALL=C

#
# Begin environment for moose-petsc-mpich-x86_64:acb1bfc
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="petsc"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-petsc-mpich-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-petsc-mpich-x86_64:acb1bfc"
export MOOSE_APPTAINER_GENERATOR_TAG="acb1bfc"
export MOOSE_APPTAINER_GENERATOR_VERSION="acb1bfc"

# Set the MPI environment
source /opt/mpi/use-mpich

# From moose-petsc
export PETSC_DIR=/opt/petsc

#
# Begin environment for moose-libmesh-mpich-x86_64:0e90306
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="libmesh"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-libmesh-mpich-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-libmesh-mpich-x86_64:0e90306"
export MOOSE_APPTAINER_GENERATOR_TAG="0e90306"
export MOOSE_APPTAINER_GENERATOR_VERSION="0e90306"

# From moose-libmesh
export LIBMESH_DIR=/opt/libmesh
if ! $CC --version | grep --quiet "clang version 16"; then
  export VTKINCLUDE_DIR=/opt/vtk/include/vtk-9.3
  export VTKLIB_DIR=/opt/vtk/lib
fi

#
# Begin environment for moose-dev-mpich-x86_64:28a1964
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="moose-dev"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-dev-mpich-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-dev-mpich-x86_64:28a1964"
export MOOSE_APPTAINER_GENERATOR_TAG="28a1964"
export MOOSE_APPTAINER_GENERATOR_VERSION="28a1964"

export PATH=/opt/miniforge3/bin:/opt/code-server/bin:$PATH
source activate /opt/miniforge3/envs/moose

export WASP_DIR=/opt/wasp
export PATH=${WASP_DIR}/bin:$PATH
# Make libtorch visible to moose
export LIBTORCH_DIR=/opt/libtorch
# Adding this to not get GPU initialization errors from MPICH
export MPIR_CVAR_ENABLE_GPU=0

#
# Begin environment for moose-dev-mpich-x86_64:28a1964
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="moose-dev"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-dev-mpich-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-dev-mpich-x86_64:28a1964"
export MOOSE_APPTAINER_GENERATOR_TAG="28a1964"
export MOOSE_APPTAINER_GENERATOR_VERSION="28a1964"

#
# Begin environment for moose-mpich-x86_64:19f1734
#
export MOOSE_APPTAINER_GENERATOR_LIBRARY="app"
export MOOSE_APPTAINER_GENERATOR_NAME="moose-mpich-x86_64"
export MOOSE_APPTAINER_GENERATOR_NAME_SUMMARY="moose-mpich-x86_64:19f1734"
export MOOSE_APPTAINER_GENERATOR_TAG="19f1734"
export MOOSE_APPTAINER_GENERATOR_VERSION="19f1734"

export PATH=/opt/moose/bin:/opt/code-server-moose/bin:$PATH
export INSTALLED_BINARIES=moose-opt:exodiff:hit
export MOOSE_LANGUAGE_SERVER=moose-opt
export INSTALLED_BINARIES=${INSTALLED_BINARIES}:moose_test-opt


make -j 4
