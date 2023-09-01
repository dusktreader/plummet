SHELL:=/bin/bash
PACKAGE_NAME:=plummet

.PHONY: install
install:
	poetry install --extras=time-machine

.PHONY: test
test: install
	poetry run pytest

.PHONY: mypy
mypy: install
	poetry run mypy ${PACKAGE_NAME} --pretty

.PHONY: lint
lint: install
	poetry run ruff check ${PACKAGE_NAME} tests

.PHONY: qa
qa: test mypy lint
	echo "All quality checks pass!"

.PHONY: format
format: install
	poetry run ruff check ${PACKAGE_NAME} tests --fix

.PHONY: publish
publish: install
	git tag v$(shell poetry version --short)
	git push origin v$(shell poetry version --short)

.PHONY: clean
clean: clean-eggs clean-build
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete
	@find . -iname '*~' -delete
	@find . -iname '*.swp' -delete
	@find . -iname '__pycache__' -delete
	@rm -r .mypy_cache
	@rm -r .pytest_cache
	@find . -name '*.egg' -print0|xargs -0 rm -rf --
	@rm -rf .eggs/
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
