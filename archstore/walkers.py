#
# Walkers


class Walker:
    def __init__(self):
        pass

    def walk(self, pdir):
        pass


class localfsWalker(Walker):
    # inherit def __init__():
    def walk(self, pdir):
        for entry in pdir.iterdir():
            if entry.is_dir():
                yield from self.walk(entry)
            else:
                yield entry


# TODO: S3 walker
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
