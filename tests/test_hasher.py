#!/usr/bin/python3
from .context import archstore
from archstore import hashers
from tempfile import TemporaryFile,TemporaryDirectory
from pathlib import Path
import io

import unittest

class Archstore_HasherTest(unittest.TestCase):
  '''Basic test cases.'''
  def test_constructor_type(self):
    h = hashers.Hasher()
    self.assertTrue(isinstance(h,hashers.Hasher))

class Archstore_localMD5Test(unittest.TestCase):
  '''Basic test cases.'''
  def test_constructor_type(self):
    h1 = hashers.localMD5Hasher()
    self.assertTrue(isinstance(h1,hashers.Hasher))
    self.assertTrue(isinstance(h1,hashers.localMD5Hasher))

  def test_empty_value(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localMD5Hasher()
      open(d + 'test1','w').close()
      # Verify that the empty tempfile hashes
      self.assertEqual(h1._hash(Path(d + 'test1')), 'd41d8cd98f00b204e9800998ecf8427e')

  def test_short_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localMD5Hasher()
      # Start over with a short message
      with open(d + 'test2', 'w') as f:
	      f.write('Hello World')
      self.assertEqual(h1._hash(Path(d+'test2')), 'b10a8db164e0754105b7a99be72e3fe5')

  def test_long_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localMD5Hasher()
      with open(d+'test3', 'w') as f:
        # Start over, message is 11 cipher-blocks long
        f.write('Hello World' * 64)
        self.assertEqual(h1._hash(Path(d+'test3')), 'd41d8cd98f00b204e9800998ecf8427e')

  def test_longer_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localMD5Hasher()
      with open(d+'test3', 'w') as f:
        # Start over, message is 11 cipher-blocks long
        f.write('Hello World' * 64)
        f.write('and more')
        self.assertEqual(h1._hash(Path(d+'test3')), 'd41d8cd98f00b204e9800998ecf8427e' )

from hashlib import sha256
class Archstore_localCryptoTest(unittest.TestCase):
  '''Basic test cases.'''
  def test_constructor_type(self):
    h1 = hashers.localCryptoHasher(sha256)
    self.assertTrue(isinstance(h1,hashers.Hasher))
    self.assertTrue(isinstance(h1,hashers.localCryptoHasher))

  def test_empty_value(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localCryptoHasher(sha256)
      open(d + 'test1','w').close()
      # Verify that the empty tempfile hashes
      self.assertEqual(h1._hash(Path(d + 'test1')), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

  def test_short_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localCryptoHasher(sha256)
      # Start over with a short message
      with open(d + 'test2', 'w') as f:
	      f.write('Hello World')
      self.assertEqual(h1._hash(Path(d+'test2')), 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e')

  def test_long_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localCryptoHasher(sha256)
      with open(d+'test3', 'w') as f:
        # Start over, message is 11 cipher-blocks long
        f.write('Hello World' * 64)
        self.assertEqual(h1._hash(Path(d+'test3')), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

  def test_longer_file(self):
    with TemporaryDirectory() as d:
      h1 = hashers.localCryptoHasher(sha256)
      with open(d+'test3', 'w') as f:
        # Start over, message is 11 cipher-blocks long
        f.write('Hello World' * 64)
        f.write('and more')
        self.assertEqual(h1._hash(Path(d+'test3')), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

if __name__ == "__main__":
  unittest.main()

