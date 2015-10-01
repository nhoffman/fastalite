import sys
import gzip
from collections import namedtuple
try:
    import bz2
except ImportError:
    bz2 = None


Seq = namedtuple('Seq', 'id, description, seq')


class Opener(object):

    """Factory for creating file objects. Transparenty opens compressed
    files for reading or writing based on suffix (.gz and .bz2 only).

    Example::

        with Opener()('in.txt') as infile, Opener('w')('out.gz') as outfile:
            outfile.write(infile.read())
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.mode = self.kwargs.get('mode') or (self.args[0] if self.args else 'r')
        self.writable = 'w' in self.mode

    def __call__(self, obj):
        if obj is sys.stdout or obj is sys.stdin:
            return obj
        elif obj == '-':
            return sys.stdout if self.writable else sys.stdin
        elif obj.endswith('.bz2'):
            if bz2 is None:
                raise ImportError(
                    'could not import bz2 module - was python built with libbz2?')
            return bz2.BZ2File(obj, *self.args, **self.kwargs)
        elif obj.endswith('.gz'):
            return gzip.open(obj, *self.args, **self.kwargs)
        else:
            return open(obj, *self.args, **self.kwargs)

    def __repr__(self):
        return '{}("{}")'.format(type(self).__name__, self.mode)


def fastalite(handle):
    """Return a sequence of namedtuple objects with attributes (id,
    description, seq) given open file-like object ``handle``

    """

    name, seq = '', ''
    for line in handle:
        if line.startswith('>'):
            if name:
                yield Seq(name.split()[0], name, seq)
            name, seq = line[1:].strip(), ''
        else:
            seq += line.strip()

    if name and seq:
        yield Seq(name.split()[0], name, seq)
