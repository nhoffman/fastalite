#!/usr/bin/env python

import os
from os import path
import inspect

import pytest

from fastalite import fastalite, fastqlite, Opener

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


def test_fastq1():
    with Opener()('testfiles/good.fastq') as infile:
        seqs = fastqlite(infile)
        assert len(list(seqs)) == 20


def test_fastq2():
    "'+' replaced with '-' on line 15"
    with Opener()('testfiles/bad1.fastq') as infile:
        seqs = fastqlite(infile)
        with pytest.raises(ValueError) as excinfo:
            list(seqs)

        assert 'line 12' in str(excinfo.value)


def test_fastq3():
    "final qual line missing"
    with Opener()('testfiles/bad2.fastq') as infile:
        seqs = fastqlite(infile)
        with pytest.raises(ValueError) as excinfo:
            list(seqs)

        assert 'line 76' in str(excinfo.value)


def test_fastq4():
    "first qual line missing one character"
    with Opener()('testfiles/bad3.fastq') as infile:
        seqs = fastqlite(infile)
        with pytest.raises(ValueError) as excinfo:
            list(seqs)

        assert 'line 0' in str(excinfo.value)
