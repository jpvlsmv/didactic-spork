#!/usr/bin/python3

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': 'Didactic Spork',
  'author': 'Joe Moore',
  'url': 'https://github.com/jpvlsmv/didactic-spork',
  'author_email': 'jpvlsmv@gmail.com',
  'version': '0.0.1',
  'install_requires': ['nose'],
  'packages': ['archstore'],
  'scripts': [],
  'name': 'didactic-spork'
}

setup(**config)
