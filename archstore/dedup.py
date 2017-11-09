# deduplicate 
from collections import namedtuple
import os
from hashlib import md5

recordClass = namedtuple('recordClass', ['path', 'md5'])
files = dict()

def fhash(x):
  hash_md5 = md5()
  with open(x,"rb") as f:
    for chunk in iter(lambda: f.read(4096), b''):
      hash_md5.update(chunk)
  return hash_md5.hexdigest()

def main():
  rootdir = '.'
  for dirName, subdirList, fileList in os.walk(rootdir):
    print(f'Found directory: {dirName}')
    for fname in fileList:
      p = os.path.join(dirName, fname)
      sz = os.stat(p).st_size
      print(f'\t{fname} ({sz} bytes)')

      if sz not in files:
        # First time we have seen this size, just record path
        files[sz] = p
      else:
        if not isinstance(files[sz], dict):
          # hash the old path, and dict it
          oldh = fhash(files[sz])
          print(f'\t\tsize {sz} seen once, {files[sz]} hash now {oldh}')
          files[sz] = { oldh: files[sz] }
        else:
          print(f'\t\tsize {sz} seen {len(files[sz])} times')

        h = fhash(p)

        if h in files[sz]:
          # Compare len(p) with len(files[sz][h]) and remove longer
          if len(p) < len(files[sz][h]): 
            print(f'Remove {files[sz][h]}')
            files[sz][h] = p
          elif len(p) == len(files[sz][h]) and p < files[sz][h]:
              print(f'Remove {files[sz][h]}')
              files[sz][h] = p
          else:
            print(f'Remove {p}')
        else:
          print(f'new hash {h}')
          files[sz][h] = p


if __name__ == "__main__":
  main()
