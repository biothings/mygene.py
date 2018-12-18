.. MyGene.py documentation master file, created by
   sphinx-quickstart on Wed Jan  8 09:57:08 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _MyGene.Info: http://mygene.info
.. _biothings_client: https://pypi.org/project/biothings-client/
.. _mygene: https://pypi.org/project/mygene/

Welcome to MyGene.py's documentation!
=====================================
MyGene.Info_ provides simple-to-use REST web services to query/retrieve gene annotation data. It's designed with simplicity
and performance emphasized. *mygene*, is an easy-to-use Python wrapper to access MyGene.Info_ services.

.. Note::
    As of v3.1.0, mygene_ Python package is now a thin wrapper of underlying biothings_client_ package,
    a universal Python client for all `BioThings APIs <http://biothings.io>`_, including MyGene.info_.
    The installation of mygene_ will install biothings_client_ automatically. The following code snippets
    are essentially equivalent:

    * Continue using mygene_ package

        .. code-block:: python

            In [1]: import mygene
            In [2]: mg = mygene.MyGeneInfo()

    * Use biothings_client_ package directly

        .. code-block:: python

            In [1]: from biothings_client import get_client
            In [2]: mg = get_client('gene')

    After that, the use of ``mg`` instance is exactly the same.


.. toctree::
   :maxdepth: 2
   index


Requirements
============
    Python >=2.7 (including python3)

    (Python 2.6 might still work, not it's not supported any more since v3.1.0.)

    biothings_client_ (>=0.2.0, install using "pip install biothings_client")

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
.. autoclass:: MyGeneInfo
    :members:
    :inherited-members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
