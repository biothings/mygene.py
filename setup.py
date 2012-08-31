import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mygene",
    version = "0.1.0",
    author = "Chunlei Wu",
    author_email = "cwu@scripps.edu",
    description = "Python Client for MyGene.Info services.",
    license = "BSD",
    keywords = "biology gene annotation web service client api",
    url = "https://bitbucket.org/newgene/mygene",
    packages=['mygene', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        'httplib2>=0.6',
    ],
)
