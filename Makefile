check:
	@pep8 docformatter docformatter.py setup.py
	@echo .
	@pep257.py docformatter docformatter.py setup.py
	@echo .
	@pylint --report=no --include-ids=yes --disable=F0401,R0914 --rcfile=/dev/null docformatter.py setup.py
	@echo .
	@python setup.py --long-description | rst2html --strict > /dev/null

coverage:
	@rm -f .coverage
	@coverage run test_docformatter.py
	@coverage report
	@coverage html
	@rm -f .coverage
	@open 'htmlcov/index.html'

readme:
	@python setup.py --long-description | rst2html --strict > README.html
	@open README.html

register:
	@python setup.py register
	@python setup.py sdist upload
	@srm ~/.pypirc
