# aeromancy-demo-housing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)

Aeromancy demo (California Housing Prices)

## Requirements and Setup

aeromancy-demo-housing requires Python >=3.11 and [`pdm`](https://pdm.fming.dev):

```bash
pip install --user pdm
```

After cloning this project, you'll need to install dependencies, switch to
a development branch, and make a directory for our dataset:

```bash
pdm install
git switch --create aeromancy-test
mkdir ingest
```

You'll want to follow the general Aeromancy setup there before running any experiments.
See the [Aeromancy repository](https://github.com/quant-aq/aeromancy/) for the
most complete and up-to-date documentation.

## Running experiments in Aeromancy

To get started, try running all experiment tasks in development mode:

```bash
pdm go --dev
```

The Aeromancy [`Action`](https://quant-aq.github.io/aeromancy/tasks/)s for these tasks live in
[`src/aeromancy_demo_housing/actions.py`](https://github.com/dmcc/aeromancy-demo-housing/blob/main/src/aeromancy_demo_housing/actions.py). Try adjusting the model in `src/aeromancy_demo_housing/actions.py` (search for
`LinearRegression`) and rerun `pdm go --dev` see how it affects your evaluation.

To see available command line options (includes options for your experiment as
well as standard Aeromancy options):

```bash
pdm help
```

To run all experiment tasks in production mode:

```bash
pdm go
```

## Common Aeromancy commands

- `pdm rerun <W&B task ID>`: Recreate the environment of a specific experiment.
  The experiment must have been run in production mode.
- `pdm aeroview <W&B artifact ID>`: View the contents of a specific W&B artifact ID.
- `pdm aeroset <version>`: Helper script to update the library version of Aeromancy.
- `pdm debug_shell`: Open a debug shell in the Docker container.

## Other development commands

- `pdm lint`: Run pre-commit linters
- `pdm test`: Run test suite
- `pdm doc`: Start doc server
- `pdm run --list`: List all available scripts
