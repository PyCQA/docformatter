check:
	pep8 docformatter.py setup.py
	pep257 docformatter.py setup.py
	pylint \
		--reports=no \
		--disable=invalid-name,too-many-arguments,too-many-locals \
		--rcfile=/dev/null \
		docformatter.py setup.py
	check-manifest
	python setup.py --long-description | rst2html --strict > /dev/null
	docformatter docformatter.py setup.py
	python -m doctest docformatter.py
	scspell docformatter.py setup.py test_docformatter.py README.rst

coverage:
	@coverage erase
	@DOCFORMATTER_COVERAGE=1 coverage run \
		--branch --parallel-mode --omit='*/site-packages/*' \
		test_docformatter.py
	@coverage combine
	@coverage report

open_coverage: coverage
	@coverage html
	@python -m webbrowser -n "file://${PWD}/htmlcov/index.html"

mutant:
	@mut.py -t docformatter -u test_docformatter -mc

readme:
	@restview --long-description --strict
