SRC_DIR	= mixver
TEST_DIR = tests
CHECK_DIRS = $(SRC_DIR) $(TEST_DIR)

.PHONY: check
check: format-check lint test ## Launch all the checks (formatting, linting, type checking)

.PHONY: format
format: ## Format repository code
	poetry run black $(CHECK_DIRS)
	poetry run isort $(CHECK_DIRS)

.PHONY: check
format-check: ## Check the code format with no actual side effects
	poetry run black --check $(CHECK_DIRS)
	poetry run isort --check $(CHECK_DIRS)

.PHONY: lint
lint: ## Launch the linting tool
# Disabled unexpected-keyword-arg since pylint complains when defining arguments in parent dataclass \
and keyword arguments in child dataclass(kw_only=True) which should be ok since python 3.10.
	poetry run pylint -j 0 -d unexpected-keyword-arg $(SRC_DIR)
	poetry run pylint -j 0 -d missing-function-docstring $(TEST_DIR)

.PHONY: test
test: ## Launch the tests
	poetry run pytest -vv --doctest-modules $(TEST_DIR)
