===========
 fastalite
===========

The simplest possible fasta parser I could come up with. The
``fastalite`` function returns an iterator of namedtuples, each with
attributes `id`, (the header line before the first whitespace)
`description` (the entire header line), and `seq` (the sequence as a
string). For example::

  from fastalite import fastalite

  with open('seqs.fasta') as infile, open('seqs.fasta.gz', 'w') as outfile:
      for seq in fastalite(infile):
          outfile.write('>{}\n{}\n'.format(seq.id, seq.seq))


The ``Opener`` class is written to be used in place of
``argparse.FileType`` to provide transparent reading and writing of
compressed files (inferred from a .gz or .bz2 suffix)::

  import argparse
  from fastalite import Opener, fastalite

  parser = argparse.ArgumentParser()
  parser.add_argument('infile', type=Opener())
  args = parser.parse_args(arguments)
  seqs = fastalite(args.infile)


Installing
==========

For now::

  pip install git+https://github.com/nhoffman/fastalite.git

