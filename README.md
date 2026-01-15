# Some Other Race PyEi

This is a project containing all of the relevant code for the Some Other Race (SOR)
summer research project.

This is also set up as a local git repository, so it will track changes over time. 


## Installation

This project uses [uv](https://docs.astral.sh/uv/getting-started/) to manage all of the 
dependencies. Once you have uv installed, you can set up the environment with:

```bash
uv sync
```

which will create a virtual environment in `.venv` and install all of the dependencies.

## Running the Code

Currently, the pipeline is set up to generate a bunch of settings files and then the 
settings files are fed to the `run_ei_cli.py` script. At the top of the settings file
is a list of tuples that are used to generate the JSON files. Some of the provided CSV
files also need to have columns added to them to be able to run the code, so, on the cluster,
run the scripts in this order:


Note: The command `rm -rf .venv` just removes the old virtual environment if it exists

```bash
rm -rf .venv
uv sync
source .venv/bin/activate
python add_2x4_columns.py
./slurm_array.sh
```

The array script handles the directory creation and submission of the jobs to the cluster.

