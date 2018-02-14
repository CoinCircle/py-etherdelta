all:
	@echo 'no default'

publish:
	rm -rf dist/
	python setup.py sdist
	twine upload dist/*
