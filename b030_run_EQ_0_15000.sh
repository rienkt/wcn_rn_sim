#!/bin/bash
#SBATCH --account=pc_aieqsim
#SBATCH --qos=lr_normal
#SBATCH --partition=lr5
#SBATCH --nodes=12
#SBATCH --cpus-per-task=4
##SBATCH --ntasks-per-node=5
## -S means reserve 4 cores per node for system tasks
#SBATCH --time=1:30:00
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

export OMP_NUM_THREADS=4
export OMP_PLACES=threads
export OMP_PROC_BIND=spread
#
echo "hello world"

export HDF5_USE_FILE_LOCKING=FALSE

SW4DIR=/global/home/users/rnakata/src/sw4_20231012_gcc11.3.0_openmpi4.1.4-gcc
SW4=${SW4DIR}/optimize_mp/sw4
ls ${SW4}

export PROJ_LIB=$HOME/src/proj/share/proj/
export PROJ_DATA=$HOME/src/proj/share/proj/
export LD_LIBRARY_PATH=$HOME/src/sqlite/lib:$HOME/src/proj/lib64:$LD_LIBRARY_PATH
export PATH=$HOME/src/sqlite/bin:$PATH

if [ -d "output_EQ_0_15000" ]; then
  rm output_EQ_0_15000/*
else
  mkdir output_EQ_0_15000
fi


#srun $HOME/src/sw4/optimize_mp/sw4 ./b020_EQ_0_15000.sw4input
mpirun ${SW4} ./b030_EQ_0_15000.sw4input
