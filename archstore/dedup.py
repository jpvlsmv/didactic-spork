#!/usr/bin/python3
# smartdedup
""" Deduplicate files without calculating hashes of every one

    With the observation that files of different sizes can never be identical,
    this module keeps track of what file sizes have been seen, and only
    computes hashes of repeat-sizes.

    TODO: Convert to module-function
    TODO: Testing
"""

import os
from hashlib import md5


class Deduper:
    def fhash(self, f, hashtype=md5):
        """Apply hashtype functions to (open) file-ish x, return the result"""
        hash_fn = hashtype()

        for chunk in iter(lambda: f.read(4096), b""):
            hash_fn.update(chunk)

        return hash_fn.hexdigest()

    def __init__(self, hashfun):
        self.hashfun = hashfun
        self.files = dict()

    def assess_file(self, pathname):
        sz = os.stat(pathname).st_size

        if sz not in self.files:
            # First time we have seen this size, just record path
            self.files[sz] = pathname
        else:
            if not isinstance(self.files[sz], dict):
                # hash the old path, and dict it
                with open(self.files[sz], "rb") as r:
                    oldh = self.fhash(r, self.hashtype)
                    self.files[sz] = {oldh: self.files[sz]}

                with open(pathname, "rb") as r:
                    h = self.fhash(r, self.hashtype)

                if h in self.files[sz]:
                    # Compare len(p) with len(self.files[sz][h]) and
                    # remove the longer of the two
                    f = self.files[sz][h]
                    if len(pathname) < len(f):
                        self.files[sz][h] = pathname
                        print(f"duplicate of {pathname} (but longer)")
                        yield (f)
                    elif len(pathname) == len(f) and pathname < f:
                        self.files[sz][h] = pathname
                        print(f"duplicate of {pathname} (but first)")
                        yield (f)
                    else:
                        print(f"duplicate of {f}")
                        yield (pathname)
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

    D = Deduper(hashfun=md5)
    for f in D.dedup("."):
        print(f"Received filename {f} to delete")
        os.unlink(f)
    """
    >>>dedup('.',md5)
    'ok'
    """
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
