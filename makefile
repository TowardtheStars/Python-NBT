
all: distribute upload

distribute:
	if [ -d dist ]; then rm -r dist; mkdir dist;fi
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*