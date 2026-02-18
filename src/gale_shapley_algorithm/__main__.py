"""Entry-point module, in case of using `python -m gale_shapley_algorithm`."""

try:
    import typer  # noqa: F401
except ImportError:
    raise SystemExit("CLI deps not installed. Install with: pip install gale-shapley-algorithm[cli]") from None

from gale_shapley_algorithm._cli.app import app

app()
