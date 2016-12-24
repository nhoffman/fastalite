#!/usr/bin/env python

import os
from os import path
import inspect

from fastalite import fastalite, Opener

outdir = 'test_output'


def mkoutdir(basedir):
    stacknames = [x[3] for x in inspect.stack()]
    testfun = [name for name in stacknames if name.startswith('test_')][0]
    pth = path.join(basedir, testfun)

    try:
        os.makedirs(pth)
    except OSError:
        pass

    return pth


def test_opener():
    fn = 'testfiles/ten.fasta'

    out = mkoutdir(outdir)

    with Opener()(fn) as infile:
        seqs = fastalite(infile)
        assert len(list(seqs)) == 10

    basename = path.join(out, path.basename(fn))
    gzout = basename + '.gz'
    bzout = basename + '.bz2'

    with Opener()(fn) as infile, Opener('w')(gzout) as outfile:
        for seq in fastalite(infile):
            outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

    with Opener()(fn) as infile, Opener('w')(bzout) as outfile:
        for seq in fastalite(infile):
            outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

    with Opener()(fn) as a, Opener()(gzout) as b, Opener()(bzout) as c:
        for sa, sb, sc in zip(fastalite(a), fastalite(b), fastalite(c)):
            assert sa.id == sb.id == sc.id
            assert sa.description == sb.description == sc.description
            assert sa.seq == sb.seq == sc.seq




