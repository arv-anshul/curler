.ONESHELL:

SHELL := /bin/bash

# Get package name from pwd
PACKAGE_NAME := $(shell pwd)  # works for (mac | linux)
.DEFAULT_GOAL := help

# UPDATE ME
PYTHON = python3
PYTHON_VENV = .venv

help:
	$(PYTHON) <(curl -sSL https://gist.githubusercontent.com/arv-anshul/84a87b6ac9b15f51b9b8d0cdeda33f5f/raw/f48d6fa8d2e5e5769af347e8baa2677cc254c5c6/make_help_decorator.py)

# -------------------------------- Builds and Installations -----------------------------

bootstrap: clean gitignore install-hooks venv ## Installs development packages, hooks, create venv

gitignore:  ## Create .gitignore file for pyhton project
	curl -sL https://www.gitignore.io/api/venv,python,JupyterNotebooks,VisualStudioCode >> .gitignore

venv-dev: venv  ## Install the package in dev mode including all dependencies inside a virtualenv.
	$(PYTHON_VENV) -m pip install .[dev];

venv:  ## Create a new virtual environment, with default name '.venv'.
	@$(PYTHON) -m venv "$(PYTHON_VENV)" || (echo "Failed to create virtual environment" && exit 1); \
	echo >&2 "Created venv in '$(PYTHON_VENV)'"; \
	echo -e "Activate your env with the command:"; \
	echo -e "\033[1;32m$$\033[0m \033[31msource $(PYTHON_VENV)/bin/activate\033[0m"; \

# ---------------------------------- Python Packaging ------------------------------------
dist: setup.py clean  ## Builds source and wheel package
	$(PYTHON) $< sdist bdist_wheel

# -------------------------------------- Run Test  --------------------------------------
test: tests  ## Run unit-test to check the package health
	$(PYTHON) -m unittest $</test_*.py

# -------------------------------------- Clean Up  --------------------------------------
.PHONY: clean
clean: clean-build clean-pyc clean-test ## Remove all build, test, coverage and Python artefacts

clean-build: ## Remove build artefacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '*.xml' -exec rm -rf {} +

clean-pyc: ## Remove Python file artefacts
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## Remove test and coverage artefacts
	rm -rf .venv
	rm -rf .tox/
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache

# ---------------------------------- Git Hooks ------------------------------------------

install-hooks: .configs/.pre-commit-config.yaml  ## Install `pre-commit-hooks` on local directory [see: https://pre-commit.com]
	$(PYTHON) -m pip install pre-commit
	pre-commit install --install-hooks -c .configs/.pre-commit-config.yaml

pre-commit-all: ## Run `pre-commit` on all files
	pre-commit run --all-files -c .configs/.pre-commit-config.yaml

pre-commit: ## Run `pre-commit` on staged files
	pre-commit run -c .configs/.pre-commit-config.yaml