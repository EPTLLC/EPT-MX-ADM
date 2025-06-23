.PHONY: help install install-dev test test-unit test-integration lint format type-check security clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

test:  ## Run all tests
	pytest

test-unit:  ## Run unit tests only
	pytest tests/unit/ -v

test-integration:  ## Run integration tests only
	pytest tests/integration/ -v

test-coverage:  ## Run tests with coverage report
	pytest --cov=. --cov-report=html --cov-report=term-missing

lint:  ## Run linting (flake8)
	flake8 .

format:  ## Format code with black and isort
	black .
	isort .

format-check:  ## Check code formatting
	black --check --diff .
	isort --check-only --diff .

type-check:  ## Run type checking with mypy
	mypy . --ignore-missing-imports

security:  ## Run security scan with bandit
	bandit -r . -x tests/

ci:  ## Run all CI checks locally
	$(MAKE) lint
	$(MAKE) format-check
	$(MAKE) type-check
	$(MAKE) test-coverage
	$(MAKE) security

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run:  ## Run the application
	python app.py

run-dev:  ## Run the application in development mode
	FLASK_ENV=development python app.py

setup-git-hooks:  ## Setup git pre-commit hooks
	echo '#!/bin/sh\nmake ci' > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit 