#!/bin/bash
#SBATCH --job-name=SOR_pyei
#SBATCH --time=03:00:00
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=5
#SBATCH --mem=4G
#SBATCH --requeue
#SBATCH --partition=duchin

settings_file=$(find settings_files -type f -name "*.json" | sort | sed -n "$((SLURM_ARRAY_TASK_ID + 1))p")

# Source the uv virtual environment if not already done
source .venv/bin/activate

base_setting_name=$(basename $settings_file)
log_file="./logs/${base_setting_name/.json/}__JOBID-${SLURM_JOB_ID}__ARRAYID-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.log"

python run_ei_cli.py --settings-file $settings_file > $log_file 2>&1
