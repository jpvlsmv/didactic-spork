#
# dupfinder
# from archstore import walkers
from hashlib import sha256


class Dupfinder:
    def __init__(self, walker, paths, hashfn=sha256):
        (self.walker, self.paths, self.hashfn) = (walker, paths, hashfn)
        self.seen_entries = dict()  # <size> -> { <hash> -> <filename> }

    def scan(self):
        for path in self.paths:
            for entry in self.walker.walk(path):
                print(f'Dupfinder examining {entry}')
                s = entry.stat().st_size

                if s not in self.seen_entries:
                    self.seen_entries[s] = entry
                    # yield nothing from this case

                else:
                    print(f'Seen size {s} before')

                if not isinstance(self.seen_entries[s], dict):
                    p = self.seen_entries[s]
                    self.seen_entries[s] = dict()
                    # We have not yet hashed the previously-seen file

                    print(f'hashing previously-seen {p}')

                    h2 = self.hashfn()
                    h2.update(p.read_bytes())
                    (self.seen_entries[s])[h2.hexdigest()] = p

                    # either way, hash the current file
                    h = self.hashfn()
                    h.update(entry.read_bytes())
                    hash = h.hexdigest()

                    if hash not in self.seen_entries[s]:
                        self.seen_entries[s][hash] = entry

                    else:
                        print(f'Seen hash {hash} before')

                        # Tiebreaker is pathlib-< overload
                        if entry < self.seen_entries[s][hash]:
                            retval = self.seen_entries[s][hash]
                            self.seen_entries[s][hash] = entry
                            yield retval
                        else:
                            yield entry

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
