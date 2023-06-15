#!/bin/tcsh

# activate environment
conda activate /usr/local/usrapps/infews/CAPOW_env
module load gurobi
source /usr/local/apps/gurobi/gurobi810/linux64/bin/gurobi.sh

#Submit job
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python wrapper.py"

conda deactivate
