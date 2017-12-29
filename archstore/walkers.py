#
# Walkers

class Walker:
  def __init__(self):
    pass

  def walk(self, pdir):
    pass

class localfsWalker(Walker):
  def walk(self, pdir):
    for entry in pdir.iterdir():
      if entry.is_dir():
        yield from self.walk(entry)
      else:
        yield entry

#TODO: S3 walker

# vim: tabstop=8 expandtab shiftwidth=2 softtabstop=2
