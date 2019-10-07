import os
import subprocess
from setuptools import setup, find_packages

subprocess.call(
    ('mkdir -p fastalite/data && '
     'git describe --tags --dirty > fastalite/data/ver.tmp'
     '&& mv fastalite/data/ver.tmp fastalite/data/ver '
     '|| rm -f fastalite/data/ver.tmp'),
    shell=True, stderr=open(os.devnull, "w"))

from fastalite import __version__

setup(
    author='Noah Hoffman',
    author_email='noah.hoffman@gmail.com',
    description='Simplest possible fasta parser',
    url='https://github.com/nhoffman/fastalite',
    name='fastalite',
    packages=find_packages(),
    package_dir={'fastalite': 'fastalite'},
    package_data={'fastalite': ['data/ver']},
    version=__version__,
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
