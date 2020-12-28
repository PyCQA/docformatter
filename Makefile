check:
	pycodestyle docformatter.py setup.py
	pydocstyle \
		--convention=pep257 \
		--add-ignore=D413 \
		docformatter.py \
		setup.py
	pylint \
		--reports=no \
		--disable=bad-continuation \
		--disable=fixme \
		--disable=import-outside-toplevel \
		--disable=inconsistent-return-statements \
		--disable=invalid-name \
		--disable=no-else-return \
		--disable=no-member \
		--disable=too-few-public-methods \
		--disable=too-many-arguments \
		--disable=too-many-boolean-expressions \
		--disable=too-many-locals \
		--disable=too-many-return-statements \
		--disable=useless-object-inheritance \
		--rcfile=/dev/null \
		docformatter.py setup.py
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
