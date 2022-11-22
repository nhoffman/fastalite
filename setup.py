import os
import subprocess
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

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
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/nhoffman/fastalite',
    name='fastalite',
    packages=find_packages(),
    package_dir={'fastalite': 'fastalite'},
    package_data={'fastalite': ['data/ver']},
    version=__version__,
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
