"""Print record descriptions given a fasta or fastq file

"""

import sys
import argparse
from fastalite import fastalite, fastqlite, Opener


def main(arguments):

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', help="Input file", type=Opener('r'))
    args = parser.parse_args(arguments)

    with args.infile as f:
        readfun = fastalite if 'fasta' in f.name else fastqlite
        try:
            for seq in readfun(f):
                print(seq.description)
        except ValueError, err:
            sys.stderr.write('Error: {}\n'.format(str(err)))
            return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
