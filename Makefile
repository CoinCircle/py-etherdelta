all:
	@echo 'no default'

publish:
	rm dist/
	python setup.py sdist
	twine upload dist/*
