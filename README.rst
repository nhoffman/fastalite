===========
 fastalite
===========

.. image:: https://travis-ci.org/nhoffman/fastalite.svg?branch=master
    :target: https://travis-ci.org/nhoffman/fastalite

The simplest possible fasta and fastq parsers I could come up with. The
``fastalite`` and ``fastqlite`` functions return an iterator of
namedtuples, each with attributes `id`, (the header line before the
first whitespace) `description` (the entire header line), and `seq`
(the sequence as a string). ``fastqlite`` output also has an attribute
``qual`` containing the quality scores. For example::

  from fastalite import fastalite

  with open('seqs.fasta') as infile, open('seqs.fasta.gz', 'w') as outfile:
      for seq in fastalite(infile):
          outfile.write('>{}\n{}\n'.format(seq.id, seq.seq))

The ``fastqlite`` parser also performs some limited error checking and
raises ``ValueError`` when it encounters a malformed record.

The ``Opener`` class is written to be used in place of
``argparse.FileType`` to provide transparent reading and writing of
compressed files (inferred from a .gz or .bz2 suffix)::

  import argparse
  from fastalite import Opener, fastalite

  parser = argparse.ArgumentParser()
  parser.add_argument('infile', type=Opener())
  args = parser.parse_args(arguments)
  seqs = fastalite(args.infile)


Installation
============

For now::

  pip install git+https://github.com/nhoffman/fastalite.git


Testing
=======

Tests require ``pytest``. Run all tests::

  python setup.py test

Pass options to pytest (eg, to prevent default capture of stdout/stderr)::

  python setup.py test --addopts '-s'
