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

files = dict()

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

def dedup(root,hashtype):
  print("ok")
  print(zip(os.walk(root)))
  for (fname, dirName) in [ (f, d) for (d, s, f) in zip(os.walk(root)) ]:
  ##for dirName, subdirList, fileList in os.walk(root):
  ##  for fname in fileList:
      print('.',sep='')
      p = os.path.join(dirName, fname)
      sz = os.stat(p).st_size

      if sz not in files:
        # First time we have seen this size, just record path
        files[sz] = p
      else:
        if not isinstance(files[sz], dict):
          # hash the old path, and dict it
          with open(files[sz]) as r:
            oldh = fhash(r,hashtype)
          files[sz] = { oldh: files[sz] }

        with open(p) as r:
          h = fhash(r,hashtype)

        if h in files[sz]:
          # Compare len(p) with len(files[sz][h]) and remove longer
          f=files[sz][h]
          if len(p) < len(f): 
            files[sz][h] = p
            print(f'rm {f}')
            yield(f)
          elif len(p) == len(f) and p < f:
              files[sz][h] = p
              print(f'rm {p}')
              yield(f)
          else:
            print(f'rm {p}')
            yield(p)
        else:
          files[sz][h] = p

if __name__ == "__main__":
  from hashlib import md5
  print("um")
  dedup('.',md5)
  '''
  >>>dedup('.',md5)
  'ok'
  '''
# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
