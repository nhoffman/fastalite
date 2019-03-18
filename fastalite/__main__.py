"""Command line interface to the fastlite package

"""

import sys
import argparse
from .fastalite import fastalite, fastqlite, Opener
from . import __version__


def count(seqs, fname):
    i = 1
    for i, seq in enumerate(seqs, 1):
        pass

    print(('{}\t{}'.format(fname, i)))


def names(seqs, fname):
    for seq in seqs:
        print(('{}\t{}'.format(fname, seq.id)))


def lengths(seqs, fname):
    for seq in seqs:
        print(('{}\t{}\t{}'.format(fname, seq.id, len(seq.seq))))


def main(arguments):

    actions = {'count': count, 'names': names, 'lengths': lengths}

    parser = argparse.ArgumentParser(
        prog='fastalite', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', choices=list(actions.keys()),
                        help="Action to perform")
    parser.add_argument('infiles', help="Input file", nargs='+',
                        metavar='infile.{fasta,fastq}[{.gz,.bz2}]',
                        type=Opener('r'))
    parser.add_argument('-V', '--version', action='version',
                        version=__version__,
                        help='Print the version number and exit')
    args = parser.parse_args(arguments)

    for infile in args.infiles:
        with infile as f:
            readfun = fastalite if 'fasta' in f.name else fastqlite
            seqs = readfun(f)
            try:
                fun = actions[args.action]
                fun(seqs, infile.name)
            except ValueError as err:
                sys.stderr.write('Error: {}\n'.format(str(err)))
                return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
