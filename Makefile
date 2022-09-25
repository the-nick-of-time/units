sources = $(wildcard units/*.py)
tests = $(wildcard tests/*.py)

.coverage: $(sources) $(tests) .coveragerc
	coverage run -m pytest --no-header
	coverage report

htmlcov/index.html: .coverage
	coverage html
