#!/usr/bin/env python3
#
# Hashers

class Hasher:
  def __init__(self):
    pass

  def size(self, file_elem):
    pass

  def hash(self, readable):
    pass


class localMD5Hasher(Hasher):
  # Inherit def __init__(self):

  def size(self, file_elem):
    return os.stat(file_elem).st_size

  def hash(self, filename):
    from hashlib import md5
    h = md5()
    with open(filename,'rb') as readable:
      for chunk in iter(lambda: readable.read(4096), b''):
        h.update(chunk)
    return h.hexdigest()

class localCryptoHasher(Hasher):
  def __init__(self, hashtype):
    self.hashtype = hashtype

  def size(self, file_elem):
    return os.stat(file_elem).st_size

  def hash(self, filename):
    h = self.hashtype()
    with open(filename,'rb') as readable:
      for chunk in iter(lambda: readable.read(4096), b''):
        h.update(chunk)
    return h.hexdigest()

#TODO: S3 walker

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
