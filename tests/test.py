#!/usr/bin/env python

import os
from os import path
from unittest import TestCase

from fastalite import fastalite, fastqlite, Opener

outdir = 'test_output'


class TestOpener(TestCase):

    def setUp(self):
        funcname = '_'.join(self.id().split('.')[-2:])
        self.fn = 'testfiles/ten.fasta'
        d = path.join(outdir, funcname)
        if not path.exists(d):
            os.makedirs(d)

        self.basename = path.join(outdir, funcname, path.basename(self.fn))

        with open(self.fn) as f:
            self.seqs = list(fastalite(f))

    def test_opener(self):
        with Opener()(self.fn) as infile:
            seqs = fastalite(infile)
            self.assertEqual(list(seqs), self.seqs)

    def test_gz(self):
        fname = self.basename + '.gz'
        with Opener('w')(fname) as outfile:
            for seq in self.seqs:
                outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

        with Opener()(fname) as infile:
            seqs = fastalite(infile)
            self.assertEqual(list(seqs), self.seqs)

    def test_bz2(self):
        fname = self.basename + '.bz2'
        with Opener('w')(fname) as outfile:
            for seq in self.seqs:
                outfile.write('>{}\n{}\n'.format(seq.description, seq.seq))

        with Opener()(fname) as infile:
            seqs = fastalite(infile)
            self.assertEqual(list(seqs), self.seqs)


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

    def test_fastq5(self):
        """Test allow_empty=True condition for fastq with empty seqs"""
        with Opener()('testfiles/good_with_truncate.fastq') as infile:
            seqs = fastqlite(infile, True)
            self.assertEqual(len(list(seqs)), 20)

    def test_fastq6(self):
        """Test allow_empty=False condition for fastq with empty seqs"""        
        with Opener()('testfiles/good_with_truncate.fastq') as infile:
            seqs = fastqlite(infile)
            self.assertRaises(ValueError, list, seqs)

