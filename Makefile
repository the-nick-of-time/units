sources = $(wildcard units/*.py)
tests = $(wildcard tests/*.py)
documentation = $(wildcard docs/*.rst) docs/conf.py

version := $(shell poetry version --short)

.coverage: $(sources) $(tests) .coveragerc
	coverage run -m pytest --no-header
	coverage report

htmlcov/index.html: .coverage
	coverage html

dist/units-$(version).tar.gz dist/units-$(version)-py3-none-any.whl: .coverage docs/_build/index.html
	poetry build

docs/_build/index.html: $(documentation) $(sources)
	VERSION=$(version) COMMIT=$(shell git rev-parse --short HEAD) sphinx-build -b html "docs" "docs/_build"
