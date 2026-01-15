#!/bin/bash

echo "Removing old environment"
rm -rf .venv
echo "Creating new python environment"
uv sync
echo "Activating environment"
source .venv/bin/activate


# Remove the old settings files
rm -rf settings_files 2>/dev/null
mkdir -p logs settings_files summary_files plots 

echo -e "*\n!.gitignore" > settings_files/.gitignore

python generate_settings.py

SIZE=$(find settings_files -type f -name "*.json" | wc -l)
CONCURRENT=25

sbatch --array=0-$(($SIZE - 1))%$CONCURRENT slurm_runner.sh

