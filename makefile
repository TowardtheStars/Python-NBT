
all: distribute upload

distribute:
	if [ -d dist ]; then rm -r dist; fi
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*