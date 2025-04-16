# Makefile to run setup.py

clean:
	python3 setup.py clean

docs:
	python3 setup.py docs

build:
	python3 setup.py build

install:
	pip install .

bdist:
	python3 setup.py bdist

dist:
	python3 setup.py dist

test:
	./tests_with_kvdb.sh

devtest:
	./tests_with_kvdb.sh dev
