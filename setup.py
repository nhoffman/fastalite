from setuptools import setup, find_packages
from fastalite import __version__

setup(
    author='Noah Hoffman',
    author_email='noah.hoffman@gmail.com',
    description='Simplest possible fasta parser',
    url='https://github.com/nhoffman/fastalite',
    name='fastalite',
    packages=find_packages(),
    package_dir={'fastalite': 'fastalite'},
    version=__version__,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],
)
