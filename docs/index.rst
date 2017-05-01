.. MyGene.py documentation master file, created by
   sphinx-quickstart on Wed Jan  8 09:57:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _MyGene.Info: http://mygene.info
.. _requests: http://docs.python-requests.org/en/latest/


Welcome to MyGene.py's documentation!
=====================================
MyGene.Info_ provides simple-to-use REST web services to query/retrieve gene annotation data. It's designed with simplicity and performance emphasized. *mygene*, is an easy-to-use Python wrapper to access MyGene.Info_ services.

.. toctree::
   :maxdepth: 2
   index

Requirements
============
    python >=2.6 (including python3)

    requests_ (install using "pip install requests")

Optional dependencies
======================
    `pandas <http://pandas.pydata.org>`_ (install using "pip install pandas") is required for returning a list of gene objects as `DataFrame <http://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe>`_.

Installation
=============

    Option 1
          pip install mygene

    Option 2
          download/extract the source code and run::

           python setup.py install

    Option 3
          install the latest code directly from the repository::

            pip install -e git+https://github.com/biothings/mygene.py#egg=mygene

Version history
===============

    `CHANGES.txt <https://raw.githubusercontent.com/SuLab/mygene.py/master/CHANGES.txt>`_

Tutorial
=========

* `ID mapping using mygene module in Python <http://nbviewer.ipython.org/6771106>`_

API
======

.. py:module:: mygene
.. autofunction:: alwayslist
.. autoattribute:: metadata
.. autoclass:: MyGeneInfo
    :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
