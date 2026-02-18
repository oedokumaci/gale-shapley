<div align="center">

<img src=./style/Gale-Shapley-Implementation.png width="800">

&nbsp;

This is a Python implementation of the celebrated Gale-Shapley (a.k.a. the Deferred Acceptance) Algorithm.

Time complexity is O(n^2), space complexity is O(n).

&nbsp;

![CI](https://github.com/oedokumaci/gale-shapley/actions/workflows/ci.yml/badge.svg)
![Docs](https://github.com/oedokumaci/gale-shapley/actions/workflows/docs.yml/badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

&nbsp;
# User Guide

## Requirements

- Python >= 3.12
- OS: Ubuntu, MacOS, Windows

## Installation

There are three easy ways to install the package.

### Install from PyPI

```bash
pip install gale-shapley
```

For CLI support:
```bash
pip install "gale-shapley[cli]"
```

For the GUI:
```bash
pip install "gale-shapley[gui]"
```

### Using Docker

An easy way to run the project is to use Docker. First, install [Docker](https://docs.docker.com/get-docker/). Then, run the following command in the project directory.
```bash
docker build -t gale-shapley .
```
This will build the Docker image. After the image is built, the following are some examples of how to run the project.

```bash
docker run --rm -it \
-v $(pwd)/config/example_config_custom_input.yaml:/app/config/config.yaml \
-v $(pwd)/logs:/app/logs \
gale-shapley
```

The `-v` option mounts the specified config file and logs directory to the container. The `--rm` option removes the container after it exits. The `-it` option is for interactive mode.

To run the GUI instead:
```bash
docker run --rm -p 8000:8000 gale-shapley uv run uvicorn gale_shapley._api.app:app --host 0.0.0.0 --port 8000
```

### Using Git

If you have git installed, simply run
```bash
git clone https://github.com/oedokumaci/gale-shapley
```
to clone the repository locally. After cloning, install the dependencies using [uv](https://github.com/astral-sh/uv):

1. `pip install uv`
2. `cd gale-shapley`
3. `uvx --from taskipy task setup`

## Usage

### Configuration

First edit the `./config/config.yaml` to your liking. Example config files can be found at `./config/example_config_*`.

### Quick Start

After configuring the `./config/config.yaml`, simply run the following command in the project directory.
```bash
uvx --from taskipy task run
```

### Detailed Usage
For a list of all the CLI arguments and options, run
```bash
uvx --from taskipy task run -- --help
```

A sample output with currently implemented CLI arguments and options is shown below.

<img src=./style/CLI-Arguments.png width="600">

&nbsp;

# Developer Guide

## Setup

This project is managed with [uv](https://github.com/astral-sh/uv) and uses [taskipy](https://github.com/taskipy/taskipy) for task running. First install uv, then clone the project and run `uvx --from taskipy task setup` in the project directory to install all dependencies.

## Development

### Pre-commit Hooks

The project uses pre-commit hooks. Run
```bash
uv run pre-commit install
```
in the project directory to install hooks to your local `.git`.
