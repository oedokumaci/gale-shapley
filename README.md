<div align="center">

<img src=./style/Gale-Shapley-Implementation.png width="800">

&nbsp;

This is a Python implementation of the celebrated Gale-Shapley (a.k.a. the Deferred Acceptance) Algorithm.

Time complexity is O(n^2), space complexity is O(n).

&nbsp;

![Tests](https://github.com/oedokumaci/gale-shapley/actions/workflows/tests.yml/badge.svg)
![Quality](https://github.com/oedokumaci/gale-shapley/actions/workflows/quality.yml/badge.svg)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

&nbsp;
# User Guide

## Requirements

- Python >= 3.9
- OS: Ubuntu, MacOS, Windows

## Installation

There are three easy ways to install the package.

### Using Docker

An easy way to run the project is to use Docker. First, install [Docker](https://docs.docker.com/get-docker/). Then, run the following command in the project directory.
```bash
docker build -t gale-shapley .
```
This will build the Docker image. After the image is built, the following are some examples of how to run the project.

```bash
docker run --rm -it \
-v $(pwd)/config/example_config_custom_input.yaml:/usr/src/app/config/config.yaml \
-v $(pwd)/logs:/usr/src/app/logs \
-e number_of_simulations=$(number_of_simulations) \
gale-shapley
```

These commands will run the project with the specified config file and number of simulations. The output can be seen in the terminal. The `-v` option mounts the specified config file and logs directory to the container. The `-e` option sets the environment variable `number_of_simulations` to the specified value. The `--rm` option removes the container after it exits. The `-it` option is for interactive mode.
You can also use Makefile recipes to run the project with Docker. See the [Makefile](#makefile) section for more information.


### Download Zip File

Pip installing the package from PyPI is not yet available. Instead, download [from this link](https://github.com/oedokumaci/gale-shapley/archive/refs/heads/main.zip) and unzip. You will also need to change the folder name from gale-shapley-main to gale-shapley (or cd into gale-shapley-main in step 2 below). 

### Using Git

If you have git installed, simply run 
```bash
git clone https://github.com/oedokumaci/gale-shapley
```
to install the package locally. After downloading, here are the steps to install the dependencies in a virtual environment using [PDM]:

1. `pip install pdm`
2. `cd gale-shapley`
3. `pdm install --prod`

## Usage

### Configuration

First edit the `./config/config.yaml` to your liking. Example config files can be found at `./config/example_config_*`.

### Quick Start

After configuring the `./config/config.yaml`, simply run the following command in the project directory.
```bash
pdm run python -m gale_shapley
```

### Detailed Usage
For a list of all the CLI arguments and options, run
```bash
pdm run python -m gale_shapley --help
```

A sample output with currently implemented CLI arguments and options is shown below.

<img src=./style/CLI-Arguments.png width="600">

&nbsp;

# Developer Guide

## Makefile
There is a Makefile in the project directory. You can run `make help` to see the available commands as below. The Makefile is also used in the CI/CD pipeline.

<img src=./style/Make.png width="600">

## Setup

This project is [PDM]-managed, which is compatible with [PEP 621](https://www.python.org/dev/peps/pep-0621) (also compatible with the <i>rejected</i> [PEP 582](https://www.python.org/dev/peps/pep-0582)). If you are a developer, first `pip install pdm` and then `git clone` the project. Next you can `pdm install` in the project directory, which will install all the dependencies in a [virtual environment](https://pdm.fming.dev/latest/usage/venv/).

## Development

### Pre-commit Hooks

The project also uses pre-commit hooks. Because the project uses [PDM], you **do not** need to `pip install pre-commit`. Instead, run directly
```bash
pdm run pre-commit install
```
in the project directory to install hooks to your local `.git`. Alternatively, you can also activate the virtual environment and run
```bash
pre-commit install
```

[PDM]: https://pdm.fming.dev
