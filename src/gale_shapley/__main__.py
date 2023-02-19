"""Entry-point module, in case of using `python -m gale_shapley`."""

import typer

from gale_shapley.cli import main

typer.run(main)
