#!/usr/bin/env python3
# Smartdedup v2
''' Remove duplicate files without calculating hashes of every one

    With the observation that files of different sizes can never be identical,
    this module keeps track of what file sizes have been seen, and only computes
    hashes of repeat-sizes.
'''

from pathlib import Path
from archstore import walkers,hashers
from itertools import chain
import os

def main(args):
    w = walkers.localfsWalker()
    h = hashers.localMD5Hasher()
    for file in chain.from_iterable( w.walk(Path(p)) for p in args.paths[0] ):
        duplicates = h.has_seen(file)
        if duplicates is not None:
            print(f'Dealing with files size {os.stat(file).st_size}:')
            keep = min(duplicates)
            for d in sorted(duplicates):
                if d!=keep:
                    print(f'Would remove {d}')
                else:
                    print(f'{d} is the path to keep')

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

    main(args)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
