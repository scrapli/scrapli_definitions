.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fmt: ## Run formatters
	python -m isort tests/
	python -m black tests/

lint: ## Run linters
	python -m yamllint definitions/
	python -m ruff check

test: ## Run unit tests
	python -m pytest tests/ -v

test-cov:  ## Run all tests with term and html coverage report
	python -m pytest tests/ -v \
	--cov=scrapli \
	--cov-report html
