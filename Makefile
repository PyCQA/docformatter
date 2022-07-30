check:
	pycodestyle docformatter.py setup.py
	pydocstyle docformatter.py setup.py
	pylint docformatter.py setup.py
	check-manifest
	rstcheck --report=1 README.rst
	docformatter docformatter.py setup.py
	python -m doctest docformatter.py

coverage:
	@coverage erase
	@DOCFORMATTER_COVERAGE=1 coverage run \
		--branch --parallel-mode --omit='*/site-packages/*,*/*pypy/*' \
		test_docformatter.py
	@coverage combine
	@coverage report --show-missing

open_coverage: coverage
	@coverage html
	@python -m webbrowser -n "file://${PWD}/htmlcov/index.html"

mutant:
	@mut.py -t docformatter -u test_docformatter -mc

readme:
	@restview --long-description --strict
