.PHONY: help vscode-settings setup update-dev update-user run project-help test pre-commit clean

help:  ## Show this help message for each Makefile recipe
ifeq ($(OS),Windows_NT)
	@findstr /R /C:"^[a-zA-Z0-9 -]\+:.*##" $(MAKEFILE_LIST) | awk -F ':.*##' '{printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' | sort
else
	@awk -F ':.*##' '/^[^ ]+:[^:]+##/ {printf "\033[1;32m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
endif

setup:  ## Setup project
	pdm install
	pdm run pre-commit install

update-dev:  ## Update project dependencies for development
	pdm update
	pdm run pre-commit autoupdate
	make test

update-user:  ## Download latest project version and dependencies for user
	git pull
	pdm sync
	make test

vscode-settings:  ## Generate VSCode settings file
	@mkdir -p .vscode
ifeq ($(OS),Windows_NT)
	@echo { > .vscode/settings.json
	@echo "    \"flake8.args\": [\"--max-line-length=88\", \"--select=C,E,F,W,B\", \"--extend-ignore=B009,E203,E501,W503\"]," >> .vscode/settings.json
	@echo "    \"python.autoComplete.extraPaths\": [\".venv/Lib/site-packages\"]," >> .vscode/settings.json
	@echo "    \"python.analysis.extraPaths\": [\".venv/Lib/site-packages\"]," >> .vscode/settings.json
	@echo "    \"python.testing.pytestPath\": \".venv/Scripts/pytest\"" >> .vscode/settings.json
	@echo } >> .vscode/settings.json
else
	@echo '{' > .vscode/settings.json
	@echo '    "flake8.args": ["--max-line-length=88", "--select=C,E,F,W,B", "--extend-ignore=B009,E203,E501,W503"],' >> .vscode/settings.json
	@echo '    "python.autoComplete.extraPaths": [".venv/lib/python$${env:PYTHON_VER}/site-packages"],' >> .vscode/settings.json
	@echo '    "python.analysis.extraPaths": [".venv/lib/python$${env:PYTHON_VER}/site-packages"],' >> .vscode/settings.json
	@echo '    "python.testing.pytestPath": ".venv/bin/pytest"' >> .vscode/settings.json
	@echo '}' >> .vscode/settings.json
endif

run:  ## Run project
	pdm run python -m gale_shapley $(number_of_simulations)

project-help:  ## Show project help
	pdm run python -m gale_shapley --help

test:  ## Run tests
	pdm run pytest tests -v

pre-commit: clean  ## Run pre-commit
	pdm run pre-commit run --all-files

clean:  ## Clean cached files
ifeq ($(OS),Windows_NT)
	del /q logs\pytest_test.log || :
	rmdir /s /q .mypy_cache || :
	rmdir /s /q .pytest_cache || :
	rmdir /s /q src\gale_shapley\__pycache__ || :
	rmdir /s /q tests\__pycache__ || :
else
	rm -f logs/pytest_test.log
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf src/gale_shapley/__pycache__
	rm -rf tests/__pycache__
endif
