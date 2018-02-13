#!/usr/bin/env python3
'''Hasher
The base Hasher class defines the (default) logic for comparing files.  The
observation that two files of different sizes can not be identical allows us
to delay calculating the hash of a file until the 2nd time a file of that
size is seen.
'''
import os

class Hasher:
  '''Base class for hashing functionality'''
  def __init__(self):
    self.__sizes_seen = dict()

  def has_seen(self, file_elem):
    '''Given a pathlike, returns None if this has never been seen,
       or a list of other pathlikes that are identical '''
    f_size = self._size(file_elem)

    if f_size not in self.__sizes_seen:
      self.__sizes_seen[f_size] = dict()
      self.__sizes_seen[f_size]["todo"] = file_elem
      return None

    if "todo" in self.__sizes_seen[f_size]:
      # "todo" is a magic tag this is the 2nd time for this size,
      # we didn't hash the file last time, so now we need to, do, and 
      # remove the "todo" key
      prev_hash = self._hash(self.__sizes_seen[f_size]["todo"])
      self.__sizes_seen[f_size][prev_hash] = set( [ self.__sizes_seen[f_size]["todo"] ] )
      del self.__sizes_seen[f_size]["todo"]

    f_hash = self._hash(file_elem)

    if f_hash not in self.__sizes_seen[f_size]:
      self.__sizes_seen[f_size] = dict({"todo": file_elem})
      self.__sizes_seen[f_size]["todo"] = file_elem
      return None

    else:
      self.__sizes_seen[f_size][f_hash].add(file_elem)
      return list(self.__sizes_seen[f_size][f_hash])

  def _size(self, file_elem):
    raise NotImplementedError

  def _hash(self, readable):
    raise NotImplementedError


class localMD5Hasher(Hasher):
  ''' File hasher that deals with local files with MD5 hash '''

  # Inherit
  # def __init__(self):
  # Inherit
  # def has_seen(self, file_elem):

  def _size(self, file_elem):
    return os.stat(file_elem).st_size

  def _hash(self, filename):
    from hashlib import md5
    h = md5()
    with open(filename,'rb') as readable:
      for chunk in iter(lambda: readable.read(4096), b''):
        h.update(chunk)
    return h.hexdigest()

class localCryptoHasher(localMD5Hasher):
  def __init__(self, hashtype):
    self.hashtype = hashtype
    super().__init__()

  # passthrough
  # def _size(self, file_elem):

  def _hash(self, filename):
    h = self.hashtype()
    with open(filename,'rb') as readable:
      for chunk in iter(lambda: readable.read(4096), b''):
        h.update(chunk)
    return h.hexdigest()

  # passthrough
  # def has_seen(self, file_elem):

# Mockup of S3 hasher:
#class s3CryptoHasher(Hasher):
#  def __init__(self, s3context):
#    self.s3context = s3context
#    super.__init__()
#
#  def _size(self, file_elem):
#    return s3context.get_object_size(file_elem)
#  def _hash(self, file_elem):
#    return s3context.object_etag(file_elem)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
