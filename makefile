#!/usr/bin/make -f

.PHONY: all tests

test:
	( cd tests ; nosetests -v )
