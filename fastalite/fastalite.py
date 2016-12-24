import sys
import gzip
from collections import namedtuple
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


def fastqlite(handle):
    """Return a sequence of namedtuple objects from a fastq file with
    attributes (id, description, seq, qual) given open file-like
    object ``handle``. This parser assumes that lines corresponding to
    sequences and quality scores are not wrapped.

    See https://doi.org/10.1093/nar/gkp1137 for a discussion of the
    fastq format.

    """

    Seq = namedtuple('Seq', ['id', 'description', 'seq', 'qual'])

    header, seq, qual, in_seq = '', [], [], True
    for line in handle:
        if line.startswith('@'):
            if header and qual:
                yield Seq(header.split()[0], header, ''.join(seq), ''.join(qual))
            header, seq, qual, in_seq = line[1:].strip(), [], [], True
        elif line.startswith('+'):
            in_seq = False
        elif in_seq:
            seq.append(line.strip())
        else:
            qual.append(line.strip())

    if header and qual:
        yield Seq(header.split()[0], header, ''.join(seq), ''.join(qual))


if __name__ == '__main__':
    with open('testfiles/276-11_S1_L001_R1_001.fastq') as f:
        for seq in fastqlite(f):
            print seq
