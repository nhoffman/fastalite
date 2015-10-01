import sys
import gzip
from collections import namedtuple
try:
    import bz2
except ImportError:
    bz2 = None


SeqLite = namedtuple('SeqLite', 'id, description, seq')


class Opener(object):

    """Factory for creating file objects. Transparenty opens compressed
    files for reading or writing based on suffix (.gz and .bz2 only).

    Keyword Arguments:
        - mode -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - bufsize -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.

    """

    def __init__(self, mode='r', bufsize=-1):
        self._mode = mode
        self._bufsize = bufsize

    def __call__(self, string):
        if string is sys.stdout or string is sys.stdin:
            return string
        elif string == '-':
            return sys.stdin if 'r' in self._mode else sys.stdout
        elif string.endswith('.bz2'):
            if bz2 is None:
                raise ImportError(
                    'could not import bz2 module - was python built with libbz2?')
            return bz2.BZ2File(
                string, self._mode, self._bufsize)
        elif string.endswith('.gz'):
            return gzip.open(
                string, self._mode, self._bufsize)
        else:
            return open(string, self._mode, self._bufsize)

    def __repr__(self):
        args = self._mode, self._bufsize
        args_str = ', '.join(repr(arg) for arg in args if arg != -1)
        return '{}({})'.format(type(self).__name__, args_str)


def fastalite(handle, limit=None):
    """
    Return a sequence of namedtupe objects given fasta format open
    file-like object `handle`. Sequence is a list if `readfile` is
    True, an iterator otherwise.
    """
    limit = limit or -1

    name, seq = '', ''
    for line in handle:
        if line.startswith('>'):
            if limit != 0:
                limit -= 1
            else:
                break

            if name:
                yield SeqLite(name.split()[0], name, seq)

            name, seq = line[1:].strip(), ''
        else:
            seq += line.strip()

    if name and seq:
        yield SeqLite(name.split()[0], name, seq)
