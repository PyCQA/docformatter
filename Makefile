# Find the executable in the venv (hopefully).
BLACK			= $(shell which black)
DOCFORMATTER	= $(shell which docformatter)
ISORT       	= $(shell which isort)

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

# This target is for use with IDE integration.
format:
	@echo -e "\n\t\033[1;32mAutoformatting $(SRCFILE) ...\033[0m\n"
	$(BLACK) --fast $(SRCFILE)
	$(ISORT) --settings-file ./pyproject.toml --atomic $(SRCFILE)
	@python docformatter.py --in-place --config ./pyproject.toml $(SRCFILE)
