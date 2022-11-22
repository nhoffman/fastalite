import sys
import gzip
from collections import namedtuple

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

try:
    import bz2
except ImportError as err:
    def bz2_open(filename, mode, *args, **kwargs):
        sys.exit(err)
else:
    bz2_open = bz2.open if hasattr(bz2, 'open') else bz2.BZ2File


class Opener(object):
    """Factory for creating file objects. Transparenty opens compressed
    files for reading or writing based on suffix (.gz and .bz2 only).

    Example::

        with Opener()('in.txt') as infile, Opener('w')('out.gz') as outfile:
            outfile.write(infile.read())
    """

    def __init__(self, mode='r', *args, **kwargs):
        self.mode = mode
        self.args = args
        self.kwargs = kwargs
        self.writable = 'w' in self.mode

    def __call__(self, obj):
        if obj is sys.stdout or obj is sys.stdin:
            return obj
        elif obj == '-':
            return sys.stdout if self.writable else sys.stdin
        else:
            openers = {'bz2': bz2_open, 'gz': gzip.open}
            __, suffix = obj.rsplit('.', 1)
            # in python3, both bz2 and gz libraries default to binary input and output
            mode = self.mode
            if sys.version_info.major == 3 and suffix in openers \
               and mode in {'w', 'r'}:
                mode += 't'
            opener = openers.get(suffix, open)
            return opener(obj, mode=mode, *self.args, **self.kwargs)


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
    return zip_longest(fillvalue=fillvalue, *args)


def fastqlite(handle, allow_empty=False):
    """Return a sequence of namedtuple objects from a fastq file with
    attributes (id, description, seq, qual) given open file-like
    object ``handle``. This parser assumes that lines corresponding to
    sequences and quality scores are not wrapped. Raises
    ``ValueError`` for malformed records. Optionally allows fastq
    files with empty strings in the sequence and quality lines 
    to pass format check. 

    See https://doi.org/10.1093/nar/gkp1137 for a discussion of the
    fastq format.

    """

    Seq = namedtuple('Seq', ['id', 'description', 'seq', 'qual'])
    for i, chunk in enumerate(grouper(handle, 4, '')):
        description, seq, plus, qual = chunk
        seq, qual = seq.strip(), qual.strip()

        if allow_empty:
            checks = [description.startswith('@'), isinstance(seq, str),
                      plus.startswith('+'), isinstance(qual, str),
                      len(seq) == len(qual)]
        else:
            checks = [description.startswith('@'), seq,
                      plus.startswith('+'), qual,
                      len(seq) == len(qual)]

        if not all(checks):
            raise ValueError('Malformed record around line {}'.format(i * 4))

        description = description[1:].strip()
        yield Seq(description.split()[0], description, seq, qual)
