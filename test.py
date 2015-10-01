#!/usr/bin/env python

from fastalite import fastalite, Opener


def main():
    fn = 'test/ten.fasta'

    with Opener()(fn) as infile:
        seqs = fastalite(infile)
        assert len(list(seqs)) == 10

    with Opener()(fn) as infile, Opener('w')(fn + '.gz') as outfile:
        for seq in fastalite(infile):
            outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

    with Opener()(fn) as infile, Opener('w')(fn + '.bz2') as outfile:
        for seq in fastalite(infile):
            outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

    with Opener()(fn) as a, Opener()(fn + '.gz') as b, Opener()(fn + '.bz2') as c:
        for sa, sb, sc in zip(fastalite(a), fastalite(b), fastalite(c)):
            assert sa.id == sb.id == sc.id
            assert sa.description == sb.description == sc.description
            assert sa.seq == sb.seq == sc.seq


if __name__ == '__main__':
    main()
