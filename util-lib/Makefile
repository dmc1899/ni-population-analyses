###############################################################################
## This makefile provides a standardised way to execute shell and other
## command line utilities.
##
## Usage:
## To run a single target called install packages:
##		make install_packages
##
## To get help use
##	make help
##
## Limitations:
## There are issues redirecting output from datacontract
## commands used to generate large documents. For example, the HTML output
## requires post-processing to remove line breaks.  Please be wary of this
## and test any new commands carefully.
###############################################################################

.PHONY: install
install: ## Create a Python Poetry environment and install all dependencies.
	@echo "Display current version of Python"
	@which python && python --version
	@echo "Lock Poetry dependencies"
	@poetry lock
	@echo "Creating virtual environment using Python poetry"
	@poetry install

.PHONY: install_pre_commit_hooks
install_pre_commit_hooks: ## Install the pre-commit hooks defined in .pre-commit-config.yaml.
	@echo "Installing pre-commit hooks"
	@poetry run pre-commit install
	@echo "Done."

.PHONY: run_precommit_checks
run_precommit_checks: ## Run pre-commit checks against all files in the code base.
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a

.PHONY: check
check: run_precommit_checks ## Run pre-commit and code quality checks against all files in the code base.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .
	@echo "🚀 Formatting code "
	@poetry run black src/
	@poetry run black tests/
	@echo "🚀 Linting code "
	@poetry run ruff check src/
	@poetry run ruff check tests/
	@echo "🚀 Static checking code "
	@poetry run pylint src/
	@poetry run pylint tests/

.PHONY: clean_build
clean_build: clean ## Destroy distributable directory and create new Python package using Poetry.
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean
clean: ## Destroy distributable directory.
	@echo "Cleaning distributable directory"
	@rm -rf dist

.PHONY: test
test: ## Test the application code using pytest
	@echo "Testing code: Running pytest with code coverage"
	@poetry run pytest -s -v --cov --cov-config=pyproject.toml --cov-report=html

.PHONY: uninstall_pre_commit_hooks
uninstall_pre_commit_hooks: ## Remove pre-commit hooks.
	@echo "uninstalling pre-commit hooks"
	@poetry run pre-commit uninstall
	@echo "Done."

.PHONY: test-docs
docs-test: ## Dry run build of documentation.
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation on local web server.
	@poetry run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
