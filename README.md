<div align="center">

<img src=./style/Gale-Shapley-Implementation.png width="800">

This is a Python implementation of the celebrated Gale-Shapley Algorithm also known as the Deferred Acceptance Algorithm.

The time complexity of the algorithm is O(n^2) and the space complexity is O(n).

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

</div>

# Developer Setup

This project is `pdm-managed`, which is compatible with [PEP 582] and [PEP 621]. If you are a developer, first `pip install pdm` and then make your Python interpreter aware of [PEP 582]. You can do this by running

```bash
pdm --pep582 >> ~/.bash_profile
```

Then `git clone` the project and run `pdm sync` in the project directory.

The project also uses pre-commit hooks. You can `pip install pre-commit` and then run
```bash
pre-commit install
```
in the project directory to install hooks to your local `.git`.

[pep 582]: https://www.python.org/dev/peps/pep-0582
[pep 621]: https://www.python.org/dev/peps/pep-0621
