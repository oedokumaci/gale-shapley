.PHONY: help setup run project-help test pre-commit clean

help: ## Show this help message for each Makefile recipe.
ifeq ($(OS),Windows_NT)
	@findstr /R /C:"^[a-zA-Z0-9 -]\+:.*##" $(MAKEFILE_LIST) | awk -F ':.*##' '{printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' | sort
else
	@awk -F ':.*##' '/^[^ ]+:[^:]+##/ {printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
endif

setup:  ## Setup project
	pdm install
	pdm run pre-commit install

run:  ## Run project
	pdm run python -m gale_shapley

project-help:  ## Show project help
	pdm run python -m gale_shapley --help

test: clean ## Run tests
	pdm run pytest tests -v

pre-commit: ## Run pre-commit
	pdm run pre-commit run --all-files

clean:  ## Clean cached files
ifeq ($(OS),Windows_NT)
	if exists .mypy_cache rmdir /s /q .mypy_cache
	if exists .pytest_cache rmdir /s /q .pytest_cache
	if exists src\gale_shapley\__pycache__ rmdir /s /q src\gale_shapley\__pycache__
	if exists tests\__pycache__ rmdir /s /q tests\__pycache__
else
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf src/gale_shapley/__pycache__
	rm -rf tests/__pycache__
endif
