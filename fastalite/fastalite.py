import sys
import gzip
from collections import namedtuple
from itertools import izip_longest
try:
    from bz2 import BZ2File
except ImportError, err:
    BZ2File = lambda x, *args, **kwargs: sys.exit(err)


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
    """Return a sequence of namedtuple objects from a fasta file with
    attributes (id, description, seq) given open file-like object
    ``handle``

    """

    Seq = namedtuple('Seq', ['id', 'description', 'seq'])

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


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def fastqlite(handle):
    """Return a sequence of namedtuple objects from a fastq file with
    attributes (id, description, seq, qual) given open file-like
    object ``handle``. This parser assumes that lines corresponding to
    sequences and quality scores are not wrapped. Raises
    ``ValueError`` for malformed records.

    See https://doi.org/10.1093/nar/gkp1137 for a discussion of the
    fastq format.

    """

    Seq = namedtuple('Seq', ['id', 'description', 'seq', 'qual'])
    for i, chunk in enumerate(grouper(handle, 4, '')):
        description, seq, plus, qual = chunk
        seq, qual = seq.strip(), qual.strip()

        checks = [description.startswith('@'), seq,
                  plus.startswith('+'), qual, len(seq) == len(qual)]

        if not all(checks):
            raise ValueError('Malformed record around line {}'.format(i * 4))

        description = description[1:].strip()
        yield Seq(description.split()[0], description, seq, qual)
