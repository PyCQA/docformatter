check:
	pep8 docformatter docformatter.py setup.py
	pep257 docformatter docformatter.py setup.py
	pylint \
		--reports=no \
		--msg-template='{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}' \
		--disable=C0103,F0401,R0913,R0914,W0622 \
		--rcfile=/dev/null \
		docformatter.py setup.py
	check-manifest --ignore=.travis.yml,Makefile,test_acid.py,tox.ini
	python setup.py --long-description | rst2html --strict > /dev/null
	docformatter docformatter docformatter.py setup.py
	python -m doctest docformatter.py
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
	@restview --long-description --strict
