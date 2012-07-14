check:
	@pep8 docformatter docformatter.py setup.py
	@echo .
	@pep257.py docformatter docformatter.py setup.py
	@echo .
	@pylint --report=no --include-ids=yes --disable=F0401,R0914 --rcfile=/dev/null docformatter.py setup.py
	@echo .
	@python setup.py --long-description | rst2html --strict > /dev/null
	@scspell docformatter docformatter.py setup.py test_docformatter.py README.rst

coverage:
	@rm -f .coverage
	@coverage run test_docformatter.py
	@coverage report
	@coverage html
	@rm -f .coverage
	@python -m webbrowser -n "file://${PWD}/htmlcov/index.html"

mutant:
	@mut.py -t docformatter -u test_docformatter -mc

readme:
	@python setup.py --long-description | rst2html --strict > README.html
	@python -m webbrowser -n "file://${PWD}/README.html"

register:
	@python setup.py register
	@python setup.py sdist upload
	@srm ~/.pypirc
