#!/bin/bash
#SBATCH --account=pc_aieqsim
#SBATCH --qos=lr_normal
#SBATCH --partition=lr6
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=4
## -S means reserve 4 cores per node for system tasks
#SBATCH --time=1:00:00
#SBATCH --job-name=berkley
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=rnakata@lbl.gov

#limit -h descriptors
#limit -h maxproc

module purge
module load gcc/11.3.0
module load openmpi/4.1.4-gcc
module load hdf5/1.12.2-gcc-p
module load lapack/3.10.1-gcc
module load proj.9/9.2.0

module list
#
echo "hello world"

export HDF5_USE_FILE_LOCKING=FALSEA
SW4DIR=/global/home/users/rnakata/src/sw4_20231012_gcc11.3.0_openmpi4.1.4-gcc

export PROJ_LIB=$HOME/src/proj/share/proj/
export PROJ_DATA=$HOME/src/proj/share/proj/
export LD_LIBRARY_PATH=$HOME/src/sqlite/lib:$HOME/src/proj/lib64:$LD_LIBRARY_PATH
export PATH=$HOME/src/sqlite/bin:$PATH
if [ -d "DATADIROUT" ]; then
  rm DATADIROUT/*
else
  mkdir DATADIROUT 
fi

SW4=${SW4DIR}/optimize_mp/sw4
ls ${SW4}

mpirun -np 48  ${SW4} ./c010_RID.sw4input
