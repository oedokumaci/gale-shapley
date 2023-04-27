.PHONY: setup run help test pre-commit clean

setup:  # Setup project
	pdm install
	pdm run pre-commit install

run:  # Run project
	pdm run python -m gale_shapley

help:  # Show project help
	pdm run python -m gale_shapley --help

test: clean # Run tests
	pdm run pytest tests -v

pre-commit: # Run pre-commit
	pdm run pre-commit run --all-files

ifeq ($(OS),Windows_NT)
clean:  # Clean cached files
	if exists .mypy_cache rmdir /s /q .mypy_cache
	if exists .pytest_cache rmdir /s /q .pytest_cache
	if exists src\gale_shapley\__pycache__ rmdir /s /q src\gale_shapley\__pycache__
	if exists tests\__pycache__ rmdir /s /q tests\__pycache__
else
clean:  # Clean cached files
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf src/gale_shapley/__pycache__
	rm -rf tests/__pycache__
endif
