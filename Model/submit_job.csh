#!/bin/tcsh

# activate environment
conda activate PyPSA

#Submit job
python wrapper.py

conda deactivate
