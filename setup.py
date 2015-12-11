import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mygene",
    version="2.3.0",
    author="Chunlei Wu",
    author_email="cwu@scripps.edu",
    description="Python Client for MyGene.Info services.",
    license="BSD",
    keywords="biology gene annotation web service client api",
    url="https://bitbucket.org/newgene/mygene",
    packages=['mygene'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        'requests>=2.3.0',
    ],
)
