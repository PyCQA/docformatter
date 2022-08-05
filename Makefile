
check:
	pycodestyle docformatter.py setup.py
	pydocstyle docformatter.py setup.py
	pylint docformatter.py setup.py
	check-manifest
	rstcheck --report=1 README.rst
	docformatter docformatter.py setup.py
	python -m doctest docformatter.py

coverage.unit:
	@echo -e "\n\t\033[1;32mRunning docformatter unit tests with coverage ...\033[0m\n"
	COVERAGE_FILE=".coverage.unit" py.test $(TESTOPTS) -m unit \
		--cov-config=pyproject.toml --cov=docformatter --cov-branch \
		--cov-report=term $(TESTFILE)

coverage.system:
	@echo -e "\n\t\033[1;32mRunning docformatter system tests with coverage ...\033[0m\n"
	COVERAGE_FILE=".coverage.system" py.test $(TESTOPTS) -m system \
		--cov-config=pyproject.toml --cov=docformatter --cov-branch \
		--cov-report=term $(TESTFILE)

coverage:
	@echo -e "\n\t\033[1;32mRunning full docformatter test suite with coverage ...\033[0m\n"
	@coverage erase
	$(MAKE) coverage.unit
	$(MAKE) coverage.system
	$(MAKE) coverage.old
	@coverage combine .coverage.unit .coverage.system .coverage.old
	@coverage xml --rcfile=pyproject.toml

coverage.old:
	COVERAGE_FILE=".coverage.old" coverage run \
		--branch --omit='*/site-packages/*,*/*pypy/*' \
		test_docformatter.py

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
