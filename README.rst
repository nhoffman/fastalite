===========
 fastalite
===========

.. image:: https://travis-ci.org/nhoffman/fastalite.svg?branch=master
    :target: https://travis-ci.org/nhoffman/fastalite

The simplest possible fasta and fastq parsers I could come up
with. Useful for simple manipulations of sequence files without
creating complex dependencies.

The ``fastalite`` and ``fastqlite`` functions return an iterator of
namedtuples, each with attributes `id`, (the header line before the
first whitespace) `description` (the entire header line), and `seq`
(the sequence as a string). ``fastqlite`` output also has an attribute
``qual`` containing the quality scores. For example::

  from fastalite import fastalite

  with open('inseqs.fasta') as infile, open('outseqs.fasta.gz', 'w') as outfile:
      for seq in fastalite(infile):
          outfile.write('>{}\n{}\n'.format(seq.id, seq.seq))

The ``fastqlite`` parser also performs some limited error checking and
raises ``ValueError`` when it encounters a malformed record.

The ``Opener`` class may be used in place of ``argparse.FileType`` to
support transparent reading and writing of compressed files (inferred
from a .gz or .bz2 suffix), for example::

  import argparse
  from fastalite import Opener, fastalite

  parser = argparse.ArgumentParser()
  parser.add_argument('infile', type=Opener())
  args = parser.parse_args(arguments)
  seqs = fastalite(args.infile)


You can perform a few actions on input files using the command line
interface. For a list of available commands::

  python -m fastalite -h


Installation
============

Install from PyPi using pip::

  pip install fastalite

Or install directly from the git repository::

  pip install git+https://github.com/nhoffman/fastalite.git


Testing
=======

Run all tests like this::

  python setup.py test
