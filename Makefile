sources = $(wildcard pyunitx/*.py)
tests = $(wildcard tests/*.py)
documentation = $(wildcard docs/*.rst) docs/conf.py

version := $(shell poetry version --short)

.coverage: $(sources) $(tests) .coveragerc
	coverage run -m pytest
	coverage report

htmlcov/index.html: .coverage
	coverage html

dist/pyunitx-$(version).tar.gz dist/pyunitx-$(version)-py3-none-any.whl: .coverage docs/_build/index.html
	poetry build

docs/_build/index.html: $(documentation) $(sources) docs/README.rst
	VERSION=$(version) COMMIT=$(shell git rev-parse --short HEAD) sphinx-build -b html "docs" "docs/_build"

docs/README.rst: README.md
	./.pandoc/pandoc-2.19.2/bin/pandoc --from=gfm --to=rst "$<" | tail -n +4 >"$@"
