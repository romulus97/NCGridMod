#!/bin/tcsh

# activate environment
conda activate /usr/local/usrapps/infews/group_env
module load gurobi

#Submit job
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python MTSDataSetup.py"

conda deactivate
