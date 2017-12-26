#!/usr/bin/python3
from .context import archstore

import unittest

class ArchstoreTest(unittest.TestCase):
  """Basic test cases."""
  def test1(self):
    self.assertEqual(1,1)

if __name__ == "__main__":
  unittest.main()
