#!/usr/bin/env python3
# Smartdedup v2
''' Remove duplicate files without calculating hashes of every one

  With the observation that files of different sizes can never be identical,
  this module keeps track of what file sizes have been seen, and only computes
  hashes of repeat-sizes.
'''
from pathlib import Path
from collections import namedtuple

def _readable_dir(p):
  return Path(p).is_dir()

def dirwalker(p):
  for entry in p.iter_dir():
    if entry.is_dir():
      yield from dirwalker(entry)
    else:
      yield entry

def main(args):
  for candidate in dirwalker(p):
    if args.dev:
      print(candidate)
      return
    if haveseen(candidate):
      fh = fhash(candidate)
      for seen in sizematches:
        if fh == seen.hash:
          if len(seen.name) < len(candidate):
            pass
      
      storehash(candidate,fh)
    else:
      marksize(candidate)
    




if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--verbose','-v',action='count')
  parser.add_argument('--noopt', '-n', action='store_true')
  parser.add_argument('--dev', '-d', action='store_true')
  parser.add_argument('paths', nargs='*', type=_readable_dir)
  args = parser.parse_args()

  if args.paths:
    args.apaths = map(Path, args.paths)
  else:
    args.apaths = [ Path().resolve() ]

  if args.dev:
    print(args)
  else:
    main(args)

# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
