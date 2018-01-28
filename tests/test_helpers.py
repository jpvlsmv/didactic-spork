#!/usr/bin/python3
from .context import archstore
from archstore import core

import unittest

class Archstore_CoreTest(unittest.TestCase):
  '''Basic test cases.'''
  def test1(self):
    self.assertEqual(1,1)

if __name__ == "__main__":
  unittest.main()
