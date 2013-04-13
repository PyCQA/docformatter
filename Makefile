check:
	pep8 docformatter docformatter.py setup.py
	pep257 docformatter docformatter.py setup.py
	pylint --report=no --include-ids=yes --disable=C0103,F0401,R0914,W0404,W0622 --rcfile=/dev/null docformatter.py setup.py
	python setup.py --long-description | rst2html --strict > /dev/null
	scspell docformatter docformatter.py setup.py test_docformatter.py README.rst

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
	@restview --long-description

register:
	@python setup.py register sdist upload
	@srm ~/.pypirc
