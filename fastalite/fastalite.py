import sys
import gzip
from collections import namedtuple
try:
    from bz2 import BZ2File
except ImportError, err:
    BZ2File = lambda x, *args, **kwargs: sys.exit(err)


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
        self.writable = 'w' in kwargs.get('mode', args[0] if args else 'r')

    def __call__(self, obj):
        if obj is sys.stdout or obj is sys.stdin:
            return obj
        elif obj == '-':
            return sys.stdout if self.writable else sys.stdin
        else:
            __, suffix = obj.rsplit('.', 1)
            opener = {'bz2': BZ2File,
                      'gz': gzip.open}.get(suffix, open)
            return opener(obj, *self.args, **self.kwargs)


def fastalite(handle):
    """Return a sequence of namedtuple objects with attributes (id,
    description, seq) given open file-like object ``handle``

    """

    header, seq = '', []
    for line in handle:
        if line.startswith('>'):
            if header:
                yield Seq(header.split()[0], header, ''.join(seq))
            header, seq = line[1:].strip(), []
        else:
            seq.append(line.strip())

    if header and seq:
        yield Seq(header.split()[0], header, ''.join(seq))
