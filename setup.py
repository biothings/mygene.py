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
    url = "http://pypi.python.org/pypi/mygene",
    packages=['mygene', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'httplib2>=0.6',
    ],
)
