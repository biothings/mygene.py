Intro
=====

MyGene.Info_ provides simple-to-use REST web services to query/retrieve gene annotation data. It's designed with simplicity and performance emphasized. *mygene*, is an easy-to-use Python wrapper to access MyGene.Info_ services.

.. _MyGene.Info: http://mygene.info


Requirements
============
    httplib2


Installation
=============

    1. pip install mygene
    2. download/extract the source code and run::
        python setup install

    3. install the latest code directly from the repository::
        pip install -e hg+https://bitbucket.org/newgene/mygene#egg=mygene


Usage
=====

::
    In [1]: import mygene

    In [2]: mg = mygene.MyGeneInfo()

    In [3]: mg.getgene(1017)
    Out[3]: {'_id': '1017', 'name': 'cyclin-dependent kinase 2', 'symbol': 'CDK2'}

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
     'refseq': {'rna': ['NM_001798.3', 'NM_052827.2']},
     'symbol': 'CDK2'}

    In [6]: mg.getgenes([1017,1018,'ENSG00000148795'])
    Out[6]: 
    [{'_id': '1017', 'name': 'cyclin-dependent kinase 2', 'symbol': 'CDK2'},
     {'_id': '1018', 'name': 'cyclin-dependent kinase 3', 'symbol': 'CDK3'},
     {'_id': '1586',
      'name': 'cytochrome P450, family 17, subfamily A, polypeptide 1',
      'symbol': 'CYP17A1'}]

    In [7]:  mg.query('cdk2', limit=5)
    Out[7]: 
    {'etag': '1358e787924ddb',
     'limit': 5,
     'rows': [{'id': '684247',
       'name': 'similar to S-phase kinase-associated protein 1A (Cyclin A/CDK2-associated protein p19) (p19A) (p19skp1)',
       'score': 2.615727663040161,
       'symbol': 'LOC684247',
       'taxid': 10116},
      {'id': '681208',
       'name': 'similar to S-phase kinase-associated protein 1A (Cyclin A/CDK2-associated protein p19) (p19A) (p19skp1)',
       'score': 2.288761615753174,
       'symbol': 'LOC681208',
       'taxid': 10116},
      {'id': '690181',
       'name': 'similar to S-phase kinase-associated protein 1A (Cyclin A/CDK2-associated protein p19) (p19A) (p19skp1)',
       'score': 2.288761615753174,
       'symbol': 'LOC690181',
       'taxid': 10116},
      {'id': '690646',
       'name': 'similar to S-phase kinase-associated protein 2 (F-box protein Skp2) (Cyclin A/CDK2-associated protein p45) (F-box/WD-40 protein 1) (FWD1)',
       'score': 1.9617958068847656,
       'symbol': 'LOC690646',
       'taxid': 10116},
      {'id': '687002',
       'name': 'similar to S-phase kinase-associated protein 2 (F-box protein Skp2) (Cyclin A/CDK2-associated protein p45) (F-box/WD-40 protein 1) (FWD1)',
       'score': 1.9617958068847656,
       'symbol': 'LOC687002',
       'taxid': 10116}],
     'skip': 0,
     'total_rows': 29}

    In [8]: mg.query('reporter:1000_at')
    Out[8]: 
    {'etag': '13574eee908e81',
     'limit': 25,
     'rows': [{'homologene': {'genes': [[9606, 5595],
         [10090, 26417],
         [10116, 50689],
         [7955, 399480],
         [3702, 837559],
         [3702, 842248]],
        'id': 55682},
       'id': '5595',
       'name': 'mitogen-activated protein kinase 3',
       'score': 8.231849670410156,
       'symbol': 'MAPK3',
       'taxid': 9606}],
     'skip': 0,
     'total_rows': 1}

    In [9]: mg.query('symbol:cdk2 AND species:human')
    Out[9]: 
    {'etag': '1358e787924ddb',
     'limit': 25,
     'rows': [{'homologene': {'genes': [[9606, 1017],
         [10090, 12566],
         [10116, 362817],
         [7227, 42453],
         [7955, 406715],
         [3702, 824036]],
        'id': 74409},
       'id': '1017',
       'name': 'cyclin-dependent kinase 2',
       'score': 71.34159851074219,
       'symbol': 'CDK2',
       'taxid': 9606}],
     'skip': 0,
     'total_rows': 1}


Contact
========
Drop us any feedback at: help@mygene.info
