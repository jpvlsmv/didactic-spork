#!/usr/bin/python3

def get_hmm():
	"""Get a thought."""
	return 'hmm...'

def hmm():
	"""Contemplation...
	>>> get_hmm()
	'hmm...'
	"""
	print(get_hmm())

if __name__ == "__main__":
	import doctest
	doctest.testmod()
