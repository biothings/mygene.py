Intro
=====

MyGene.Info_ provides simple-to-use REST web services to query/retrieve gene annotation data. It's designed with simplicity and performance emphasized. *mygene*, is an easy-to-use Python wrapper to access MyGene.Info_ services.

.. _MyGene.Info: http://mygene.info
.. _requests: http://docs.python-requests.org/en/latest/

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

            pip install -e hg+https://bitbucket.org/newgene/mygene#egg=mygene

Version history
===============

    `CHANGES.txt <https://bitbucket.org/newgene/mygene/raw/tip/CHANGES.txt>`_

Tutorial
=========

* `ID mapping using mygene module in Python <http://nbviewer.ipython.org/6771106>`_

Documentation
=============

    http://mygene-py.readthedocs.org/

Usage
=====

.. code-block:: python

    In [1]: import mygene

    In [2]: mg = mygene.MyGeneInfo()

    In [3]: mg.getgene(1017)
    Out[3]:
    {'_id': '1017',
     'entrezgene': 1017,
     'name': 'cyclin-dependent kinase 2',
     'symbol': 'CDK2',
     'taxid': 9606}

    In [4]: mg.getgene(1017, 'name,symbol,refseq')
    Out[4]:
    {'_id': '1017',
     'name': 'cyclin-dependent kinase 2',
     'refseq': {'genomic': ['AC_000144.1',
       'NC_000012.11',
       'NG_028086.1',
       'NT_029419.12',
       'NW_001838059.1'],
      'protein': ['NP_001789.2', 'NP_439892.2'],
      'rna': ['NM_001798.3', 'NM_052827.2']},
     'symbol': 'CDK2'}

    In [5]: mg.getgene(1017, 'name,symbol,refseq.rna')
    Out[5]:
    {'_id': '1017',
     'name': 'cyclin-dependent kinase 2',
     'refseq': {'rna': ['NM_001798', 'NM_052827']},
     'symbol': 'CDK2'}


    In [6]: mg.getgenes([1017,1018,'ENSG00000148795'])
    Out[6]:
    [{'_id': '1017',
      'entrezgene': 1017,
      'name': 'cyclin-dependent kinase 2',
      'query': '1017',
      'symbol': 'CDK2',
      'taxid': 9606},
     {'_id': '1018',
      'entrezgene': 1018,
      'name': 'cyclin-dependent kinase 3',
      'query': '1018',
      'symbol': 'CDK3',
      'taxid': 9606},
     {'_id': '1586',
      'entrezgene': 1586,
      'name': 'cytochrome P450, family 17, subfamily A, polypeptide 1',
      'query': 'ENSG00000148795',
      'symbol': 'CYP17A1',
      'taxid': 9606}]

    In [7]: mg.getgenes([1017,1018,'ENSG00000148795'], as_dataframe=True)
    Out[7]:
                      _id  entrezgene  \
    query
    1017             1017        1017
    1018             1018        1018
    ENSG00000148795  1586        1586

                                                                  name   symbol  \
    query
    1017                                     cyclin-dependent kinase 2     CDK2
    1018                                     cyclin-dependent kinase 3     CDK3
    ENSG00000148795  cytochrome P450, family 17, subfamily A, polyp...  CYP17A1

                     taxid
    query
    1017              9606
    1018              9606
    ENSG00000148795   9606

    [3 rows x 5 columns]

    In [8]:  mg.query('cdk2', size=5)
    Out[8]:
    {'hits': [{'_id': '1017',
       '_score': 373.24667,
       'entrezgene': 1017,
       'name': 'cyclin-dependent kinase 2',
       'symbol': 'CDK2',
       'taxid': 9606},
      {'_id': '12566',
       '_score': 353.90176,
       'entrezgene': 12566,
       'name': 'cyclin-dependent kinase 2',
       'symbol': 'Cdk2',
       'taxid': 10090},
      {'_id': '362817',
       '_score': 264.88477,
       'entrezgene': 362817,
       'name': 'cyclin dependent kinase 2',
       'symbol': 'Cdk2',
       'taxid': 10116},
      {'_id': '52004',
       '_score': 21.221401,
       'entrezgene': 52004,
       'name': 'CDK2-associated protein 2',
       'symbol': 'Cdk2ap2',
       'taxid': 10090},
      {'_id': '143384',
       '_score': 18.617256,
       'entrezgene': 143384,
       'name': 'CDK2-associated, cullin domain 1',
       'symbol': 'CACUL1',
       'taxid': 9606}],
     'max_score': 373.24667,
     'took': 10,
     'total': 28}

    In [9]: mg.query('reporter:1000_at')
    Out[9]:
    {'hits': [{'_id': '5595',
       '_score': 11.163337,
       'entrezgene': 5595,
       'name': 'mitogen-activated protein kinase 3',
       'symbol': 'MAPK3',
       'taxid': 9606}],
     'max_score': 11.163337,
     'took': 6,
     'total': 1}

    In [10]: mg.query('symbol:cdk2', species='human')
    Out[10]:
    {'hits': [{'_id': '1017',
       '_score': 84.17707,
       'entrezgene': 1017,
       'name': 'cyclin-dependent kinase 2',
       'symbol': 'CDK2',
       'taxid': 9606}],
     'max_score': 84.17707,
     'took': 27,
     'total': 1}

    In [11]: mg.querymany([1017, '695'], scopes='entrezgene', species='human')
    Finished.
    Out[11]:
    [{'_id': '1017',
      'entrezgene': 1017,
      'name': 'cyclin-dependent kinase 2',
      'query': '1017',
      'symbol': 'CDK2',
      'taxid': 9606},
     {'_id': '695',
      'entrezgene': 695,
      'name': 'Bruton agammaglobulinemia tyrosine kinase',
      'query': '695',
      'symbol': 'BTK',
      'taxid': 9606}]

    In [12]: mg.querymany([1017, '695'], scopes='entrezgene', species=9606)
    Finished.
    Out[12]:
    [{'_id': '1017',
      'entrezgene': 1017,
      'name': 'cyclin-dependent kinase 2',
      'query': '1017',
      'symbol': 'CDK2',
      'taxid': 9606},
     {'_id': '695',
      'entrezgene': 695,
      'name': 'Bruton agammaglobulinemia tyrosine kinase',
      'query': '695',
      'symbol': 'BTK',
      'taxid': 9606}]

    In [13]: mg.querymany([1017, '695'], scopes='entrezgene', species=9606, as_dataframe=True)
    Finished.
    Out[13]:
            _id  entrezgene                                       name symbol  \
    query
    1017   1017        1017                  cyclin-dependent kinase 2   CDK2
    695     695         695  Bruton agammaglobulinemia tyrosine kinase    BTK

           taxid
    query
    1017    9606
    695     9606

    [2 rows x 5 columns]

    In [14]: mg.querymany([1017, '695', 'NA_TEST'], scopes='entrezgene', species='human')
    Finished.
    Out[14]:
    [{'_id': '1017',
      'entrezgene': 1017,
      'name': 'cyclin-dependent kinase 2',
      'query': '1017',
      'symbol': 'CDK2',
      'taxid': 9606},
     {'_id': '695',
      'entrezgene': 695,
      'name': 'Bruton agammaglobulinemia tyrosine kinase',
      'query': '695',
      'symbol': 'BTK',
      'taxid': 9606},
     {'notfound': True, 'query': 'NA_TEST'}]

    # query all human kinases using fetch_all parameter:
    In [15]: kinases = mg.query('name:kinase', species='human', fetch_all=True)
    In [16]: kinases
    Out [16]" <generator object _fetch_all at 0x7fec027d2eb0>

    # kinases is a Python generator, now you can loop through it to get all 1073 hits:
    In [16]: for gene in kinases:
       ....:     print gene['_id'], gene['symbol']
    Out [16]: <output omitted here>


Contact
========
Drop us any feedback at: help@mygene.info or on twitter `@mygeneinfo <https://twitter.com/mygeneinfo>`_.
