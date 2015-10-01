===========
 fastalite
===========

The simplest possible fasta parser I could come up with. The
``fastalite`` function returns an iterator of namedtuples, each with
attributes `id`, (the header line before the first whitespace)
`description` (the entire header line), and `seq` (the sequence as a
string).

The ``Opener`` class is written to be used in place of
``argparse.FileType`` to provide transparent reading and writing of
compressed files (inferred from a .gz or .bz2 suffix).

For example::

  from fastalite import Opener, fastalite

  with Opener()('seqs.fasta') as infile, Opener('w')('seqs.fasta.gz') as outfile:
      for seq in fastalite(infile):
          outfile.write('>{}\n{}\n'.format(seq.id, seq.seq))


Installing
==========

For now::

  pip install git+https://github.com/nhoffman/fastalite.git

