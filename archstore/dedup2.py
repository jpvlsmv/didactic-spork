#!/usr/bin/env python3
# Smartdedup v2
''' Remove duplicate files without calculating hashes of every one

  With the observation that files of different sizes can never be identical,
  this module keeps track of what file sizes have been seen, and only computes
  hashes of repeat-sizes.
'''

from pathlib import Path
from archstore import walkers,dupfinder

def main(args):
  w = walkers.localfsWalker()
  d = dupfinder.Dupfinder(w, args.paths[0])
  for duplicate in d.scan():
    print(f'Would remove {duplicate}')

if __name__ == "__main__":
  import argparse

  def _readable_dir(p):
    if Path(p).is_dir():
      return Path(p)
    else:
      raise argparse.ArgumentTypeError(f'{p} is not a valid directory')
    
  parser = argparse.ArgumentParser()
  parser.add_argument('--verbose','-v',action='count')
  parser.add_argument('--noopt', '-n', action='store_true')
  parser.add_argument('--dev', '-d', action='store_true')
  parser.add_argument('paths', nargs='*', type=_readable_dir, action='append')
  args = parser.parse_args()

  if args.dev:
    print(args)

  if not args.paths:
    args.paths = [ Path().resolve() ]

  if args.dev:
    print(args)

  main(args)

# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
