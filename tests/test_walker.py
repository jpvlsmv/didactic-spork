#!/usr/bin/python3
from .context import archstore

import unittest

class WalkerTest(unittest.TestCase):
  def test_constructor_type(self):
    '''Verify that the default constructor returns a proper object'''
    from archstore import walkers
    w = walkers.Walker()
    self.assertTrue(isinstance(w,walkers.Walker))

class localfsWalkerTest(unittest.TestCase):
  def test_constructor_type(self):
    '''Verify that the default constructor returns a proper object'''
    from archstore import walkers
    w = walkers.localfsWalker()
    self.assertTrue(isinstance(w,walkers.localfsWalker))
    self.assertTrue(isinstance(w,walkers.Walker))
  def test_walk_empty_tmpdir(self):
    from tempfile import TemporaryDirectory
    from pathlib import Path
    from archstore import walkers
    w = walkers.localfsWalker()
    with TemporaryDirectory() as T:
      self.assertListEqual(list(w.walk(Path(T))), list())


if __name__ == "__main__":
  unittest.main()
