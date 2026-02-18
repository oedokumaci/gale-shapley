"""Entry-point module, in case of using `python -m gale_shapley`."""

try:
    import typer
except ImportError:
    raise SystemExit("CLI deps not installed. Install with: pip install gale-shapley[cli]") from None

from gale_shapley._cli.app import main

typer.run(main)
