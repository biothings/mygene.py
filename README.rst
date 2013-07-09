Intro
=====

MyGene.Info_ provides simple-to-use REST web services to query/retrieve gene annotation data. It's designed with simplicity and performance emphasized. *mygene*, is an easy-to-use Python wrapper to access MyGene.Info_ services.

.. _MyGene.Info: http://mygene.info
.. _httplib2: http://code.google.com/p/httplib2/

Requirements
============
    httplib2_ (install using "pip install httplib2")


Installation
=============

    Option 1
          pip install mygene

    Options 2
          download/extract the source code and run::
           python setup install

    Option 3
          install the latest code directly from the repository::
            pip install -e hg+https://bitbucket.org/newgene/mygene#egg=mygene


Usage
=====

::

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


    In [7]:  mg.query('cdk2', size=5)
    Out[7]:
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

    In [8]: mg.query('reporter:1000_at')
    Out[8]:
    {'hits': [{'_id': '5595',
       '_score': 11.163337,
       'entrezgene': 5595,
       'name': 'mitogen-activated protein kinase 3',
       'symbol': 'MAPK3',
       'taxid': 9606}],
     'max_score': 11.163337,
     'took': 6,
     'total': 1}

    In [9]: mg.query('symbol:cdk2', species='human')
    Out[9]:
    {'hits': [{'_id': '1017',
       '_score': 84.17707,
       'entrezgene': 1017,
       'name': 'cyclin-dependent kinase 2',
       'symbol': 'CDK2',
       'taxid': 9606}],
     'max_score': 84.17707,
     'took': 27,
     'total': 1}

    In [10]: mg.querymany([1017, '695'], scopes='entrezgene', species='human')
    querying 1-2... done.
    Finished.
    Out[10]:
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

    In [11]: mg.querymany([1017, '695'], scopes='entrezgene', species=9606)
    querying 1-2... done.
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

    In [12]: mg.findgenes([1017, '695', 'NA_TEST'], scopes='entrezgene', species='human')
    querying 1-3...
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
      'taxid': 9606},
     {'notfound': True, 'query': 'NA_TEST'}]




Contact
========
Drop us any feedback at: help@mygene.info
