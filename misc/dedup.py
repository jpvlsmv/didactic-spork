#!/usr/bin/python3
# smartdedup  
'''
  Deduplicate files without calculating hashes of every one

  With the observation that files of different sizes can never be identical,
  this module keeps track of what file sizes have been seen, and only computes
  hashes of repeat-sizes.

  TODO: Convert to module-function
  TODO: Testing
'''
import os
from hashlib import md5


def fhash(f,hashtype=md5):
  ''' Apply hashtype functions to (open) file-ish x, and return the result 
  >>> from io import BytesIO

  Check that we get the correct hash of empty:
  >>> fhash(BytesIO(b''),md5)
  'd41d8cd98f00b204e9800998ecf8427e'

  Check that chunking is correct (5 chunks here):
  >>> fhash(BytesIO(b'hello'*4096),md5)
  'c21e4dada5bc00c358683211282c53f7'

  Check that chunking is correct (5 chunks and a partial here):
  >>> fhash(BytesIO(b'hello'*4097),md5)
  'ff072cf63ffe673bb40785c11c74575f'

  '''
  hash_fn = hashtype()

  for chunk in iter(lambda: f.read(4096), b''):
    hash_fn.update(chunk)

  return hash_fn.hexdigest()

class Deduper():

  files = dict()

  def assess_file(self, pathname):
    sz = os.stat(pathname).st_size
  
    if sz not in self.files:
      # First time we have seen this size, just record path
      self.files[sz] = pathname
    else:
      if not isinstance(self.files[sz], dict):
        # hash the old path, and dict it
        with open(self.files[sz],"rb") as r:
          oldh = fhash(r,self.hashtype)
          self.files[sz] = { oldh: self.files[sz] }

      with open(pathname,"rb") as r:
        h = fhash(r,self.hashtype)
  
      if h in self.files[sz]:
        # Compare len(p) with len(self.files[sz][h]) and remove longer
        f=self.files[sz][h]
        if len(pathname) < len(f): 
          self.files[sz][h] = pathname
          print(f'duplicate of {pathname} (but longer length)')
          yield(f)
        elif len(pathname) == len(f) and pathname < f:
            self.files[sz][h] = pathname
            print(f'duplicate of {pathname} (but sorted first)')
            yield(f)
        else:
          print(f'duplicate of {f}')
          yield(pathname)
      else:
        self.files[sz][h] = pathname

  def dedup(self, root, hashtype):
    self.hashtype = hashtype
    for dirName, subdirList, fileList in os.walk(root):
      for fname in fileList:
        p = os.path.join(dirName, fname)
        yield from self.assess_file(p)

if __name__ == "__main__":
  from hashlib import md5
  D = Deduper()
  for f in D.dedup('.',md5):
    print(f'Received filename {f} to delete')
    os.unlink(f)
  '''
  >>>dedup('.',md5)
  'ok'
  '''
# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
