#!/usr/bin/env python

import os
from os import path
import inspect
from unittest import TestCase

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


class TestOpener(TestCase):

    def test_opener(self):
        fn = 'testfiles/ten.fasta'

        out = mkoutdir(outdir)

        with Opener()(fn) as infile:
            seqs = fastalite(infile)
            self.assertEqual(len(list(seqs)), 10)

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
                self.assertTrue(sa.id == sb.id == sc.id)
                self.assertTrue(sa.description == sb.description == sc.description)
                self.assertTrue(sa.seq == sb.seq == sc.seq)


class TestFastq(TestCase):

    def test_fastq1(self):
        with Opener()('testfiles/good.fastq') as infile:
            seqs = fastqlite(infile)
            self.assertEqual(len(list(seqs)), 20)

    def test_fastq2(self):
        # "'+' replaced with '-' on line 15"
        with Opener()('testfiles/bad1.fastq') as infile:
            seqs = fastqlite(infile)
            self.assertRaises(ValueError, list, seqs)

    def test_fastq3(self):
        # "final qual line missing"
        with Opener()('testfiles/bad2.fastq') as infile:
            seqs = fastqlite(infile)
            self.assertRaises(ValueError, list, seqs)

    def test_fastq4(self):
        # "first qual line missing one character"
        with Opener()('testfiles/bad3.fastq') as infile:
            seqs = fastqlite(infile)
            self.assertRaises(ValueError, list, seqs)
