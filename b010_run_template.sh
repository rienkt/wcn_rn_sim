#!/bin/bash
#SBATCH --account=pc_aieqsim
#SBATCH --qos=lr_normal
#SBATCH --partition=lr4
#SBATCH --nodes=4
##SBATCH --ntasks-per-node=4
## -S means reserve 4 cores per node for system tasks
#SBATCH --time=2:00:00
#SBATCH --job-name=berkley
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=rnakata@lbl.gov

#limit -h descriptors
#limit -h maxproc

module load gcc/11.3.0
#module load openmpi
module load openmpi
module load lapack
module load hdf5
module load proj.9
#
echo "hello world"

#export HDF5_USE_FILE_LOCKING=FALSEA

export PROJ_LIB=$HOME/src/proj/share/proj/
export PROJ_DATA=$HOME/src/proj/share/proj/
export LD_LIBRARY_PATH=$HOME/src/sqlite/lib:$HOME/src/proj/lib64:$LD_LIBRARY_PATH
export PATH=$HOME/src/sqlite/bin:$PATH
if [ -d "output_SID" ]; then
  rm output_SID/*
else
  mkdir output_SID
fi
srun $HOME/src/sw4/optimize_mp/sw4 ./b010_SID.sw4input
