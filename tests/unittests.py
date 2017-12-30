#!/usr/bin/python3
from .context import archstore

import unittest

class WalkerTest(unittest.TestCase):
  def test1(self):
    from .context.archstore import walkers
    w = walkers.Walker()
    self.assert(isinstance(w,walkers.Walker))

class localfsWalkerTest(unittest.TestCase):
  def test1(self):
    from .context.archstore import walkers
    w = walkers.localfsWalker()
    self.assert(isinstance(w,walkers.localfsWalker))
    self.assert(isinstance(w,walkers.Walker))
  def test2(self):
    import tempfile
    from .context.archstore import walkers
    w = walkers.localfsWalker()
    with tempfile.TemporaryDir() as T:
      self.assert(w.walk(Path(T)) == [ ] )

class ArchstoreTest(unittest.TestCase):
  """Basic test cases."""
  def test1(self):
    self.assertEqual(1,1)

if __name__ == "__main__":
  unittest.main()
