<div align="center">

<img src=./style/Gale-Shapley-Implementation.png width="800">

<img src=./style/Algo.png width="800">

&nbsp;

This is a Python implementation of the celebrated Gale-Shapley (a.k.a. the Deferred Acceptance) Algorithm.

Time complexity is O(n^2), space complexity is O(n).

&nbsp;

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

</div>

# Developer Setup

This project is [PDM]-managed, which is compatible with [PEP 582] and [PEP 621]. If you are a developer, first `pip install pdm` and then make your Python interpreter aware of [PEP 582]. If you are using bash, you can do this by running

```bash
pdm --pep582 >> ~/.bash_profile
```

Similarly, for zsh run

```bash
pdm --pep582 >> ~/.zshrc
```
Then `git clone` the project and run `mkdir __pypackages__` in the project directory. This lets [PDM] know that you are using [PEP 582] instead of virtualenv. Now you can run `pdm sync`, which will install all the dependencies in the project directory. Sample output is shown below.

<img src=./style/PDM-Sync.png width="800">

In order to configure your IDE to support [PEP 582], you can follow the instructions [here](https://pdm.fming.dev/docs/pep582/).

&nbsp;

The project also uses pre-commit hooks. Because the project uses [PDM], you **do not** need to `pip install pre-commit`. Instead, run directly
```bash
pdm run pre-commit install
```
in the project directory to install hooks to your local `.git`.

[pep 582]: https://www.python.org/dev/peps/pep-0582
[pep 621]: https://www.python.org/dev/peps/pep-0621
[PDM]: https://pdm.fming.dev
