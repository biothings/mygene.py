'''
Python Client for MyGene.Info services
'''
from biothings_client import get_client

class MyGeneInfo(get_client('gene', instance=False)):
    pass

DOCSTRINGS = {
    'getgene': '''Return the gene object for the give geneid.
        This is a wrapper for GET query of "/gene/<geneid>" service.

        :param geneid: entrez/ensembl gene id, entrez gene id can be either
                       a string or integer
        :param fields: fields to return, a list or a comma-separated string.
                        If **fields="all"**, all available fields are returned
        :param species: optionally, you can pass comma-separated species names
                        or taxonomy ids
        :param email: optionally, pass your email to help us to track usage
        :param filter: alias for **fields** parameter

        :return: a gene object as a dictionary, or None if geneid is not valid.

        :ref: http://docs.mygene.info/en/latest/doc/data.html for available
             fields, extra *kwargs* and more.

        Example:

        >>> mg.getgene(1017, email='abc@example.com')
        >>> mg.getgene('1017', fields='symbol,name,entrezgene,refseq')
        >>> mg.getgene('1017', fields='symbol,name,entrezgene,refseq.rna')
        >>> mg.getgene('1017', fields=['symbol', 'name', 'pathway.kegg'])
        >>> mg.getgene('ENSG00000123374', fields='all')

        .. Hint:: The supported field names passed to **fields** parameter can be found from
                  any full gene object (when **fields="all"**). Note that field name supports dot
                  notation for nested data structure as well, e.g. you can pass "refseq.rna" or
                  "pathway.kegg".
        ''',
    'getgenes': '''Return the list of gene objects for the given list of geneids.
        This is a wrapper for POST query of "/gene" service.

        :param geneids: a list/tuple/iterable or comma-separated entrez/ensembl gene ids
        :param fields: fields to return, a list or a comma-separated string.
                        If **fields="all"**, all available fields are returned
        :param species: optionally, you can pass comma-separated species names
                        or taxonomy ids
        :param email: optionally, pass your email to help us to track usage
        :param filter: alias for fields
        :param as_dataframe: if True, return object as DataFrame (requires Pandas).
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.

        :return: a list of gene objects or a pandas DataFrame object (when **as_dataframe** is True)

        :ref: http://mygene.info/doc/annotation_service.html for available
                fields, extra *kwargs* and more.

        Example:

        >>> mg.getgenes([1017, '1018','ENSG00000148795'], email='abc@example.com')
        >>> mg.getgenes([1017, '1018','ENSG00000148795'], fields="entrezgene,uniprot")
        >>> mg.getgenes([1017, '1018','ENSG00000148795'], fields="all")
        >>> mg.getgenes([1017, '1018','ENSG00000148795'], as_dataframe=True)

        .. Hint:: A large list of more than 1000 input ids will be sent to the backend
                  web service in batches (1000 at a time), and then the results will be
                  concatenated together. So, from the user-end, it's exactly the same as
                  passing a shorter list. You don't need to worry about saturating our
                  backend servers.
        ''',
    'query': '''Return  the query result.
        This is a wrapper for GET query of "/query?q=<query>" service.

        :param q: a query string, detailed query syntax `here <http://mygene.info/doc/query_service.html#query-syntax>`_
        :param fields: fields to return, a list or a comma-separated string.
                        If **fields="all"**, all available fields are returned
        :param species: optionally, you can pass comma-separated species names
                        or taxonomy ids. Default: human,mouse,rat.
        :param size:   the maximum number of results to return (with a cap
                       of 1000 at the moment). Default: 10.
        :param skip:   the number of results to skip. Default: 0.
        :param sort:   Prefix with "-" for descending order, otherwise in ascending order.
                       Default: sort by matching scores in decending order.
        :param entrezonly: if True, return only matching entrez genes, otherwise, including matching
                           Ensemble-only genes (those have no matching entrez genes).
        :param email: optionally, pass your email to help us to track usage
        :param as_dataframe: if True, return object as DataFrame (requires Pandas).
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.
        :param fetch_all: if True, return a generator to all query results (unsorted).  This can provide a very fast return of
                         all hits from a large query.
                         Server requests are done in blocks of 1000 and yielded individually.  Each 1000 block of results
                         must be yielded within 1 minute, otherwise the request will expire on the server side.

        :return: a dictionary with returned gene hits or a pandas DataFrame object (when **as_dataframe** is True)

        :ref: http://mygene.info/doc/query_service.html for available
              fields, extra *kwargs* and more.

        Example:

        >>> mg.query('cdk2')
        >>> mg.query('reporter:1000_at')
        >>> mg.query('symbol:cdk2', species='human')
        >>> mg.query('symbol:cdk*', species=10090, size=5, as_dataframe=True)
        >>> mg.query('q=chrX:151073054-151383976', species=9606)

        ''',
    'querymany': '''Return the batch query result.
        This is a wrapper for POST query of "/query" service.

        :param qterms: a list/tuple/iterable of query terms, or a string of comma-separated query terms.
        :param scopes:  type of types of identifiers, either a list or a comma-separated fields to specify type of
                       input qterms, e.g. "entrezgene", "entrezgene,symbol", ["ensemblgene", "symbol"].
                       Refer to `official MyGene.info docs <http://mygene.info/doc/query_service.html#available_fields>`_ for full list
                       of fields.
        :param fields: fields to return, a list or a comma-separated string.
                        If **fields="all"**, all available fields are returned
        :param species: optionally, you can pass comma-separated species names
                          or taxonomy ids. Default: human,mouse,rat.
        :param entrezonly:  if True, return only matching entrez genes, otherwise, including matching
                             Ensemble-only genes (those have no matching entrez genes).

        :param returnall:   if True, return a dict of all related data, including dup. and missing qterms
        :param verbose:     if True (default), print out infomation about dup and missing qterms
        :param email: optionally, pass your email to help us to track usage
        :param as_dataframe: if True, return object as DataFrame (requires Pandas).
        :param df_index: if True (default), index returned DataFrame by 'query',
                         otherwise, index by number. Only applicable if as_dataframe=True.

        :return: a list of gene objects or a pandas DataFrame object (when **as_dataframe** is True)

        :ref: http://mygene.info/doc/query_service.html for available
              fields, extra *kwargs* and more.

        Example:

        >>> mg.querymany(['DDX26B', 'CCDC83'], scopes='symbol', species=9606)
        >>> mg.querymany(['1255_g_at', '1294_at', '1316_at', '1320_at'], scopes='reporter')
        >>> mg.querymany(['NM_003466', 'CDK2', 695, '1320_at', 'Q08345'],
        ...              scopes='refseq,symbol,entrezgene,reporter,uniprot', species='human')
        >>> mg.querymany(['1255_g_at', '1294_at', '1316_at', '1320_at'], scopes='reporter',
        ...              fields='ensembl.gene,symbol', as_dataframe=True)

        .. Hint:: :py:meth:`querymany` is perfect for doing id mappings.

        .. Hint:: Just like :py:meth:`getgenes`, passing a large list of ids (>1000) to :py:meth:`querymany` is perfectly fine.

        ''',
    'metadata': '''Return a dictionary of MyGene.info metadata.

        Example:

        >>> metadata = mg.metadata

        ''',
    'get_fields': '''Return all available fields can be return from MyGene.info services.

        This is a wrapper for http://mygene.info/metadata/fields

        :param search_term: an optional string to search (case insensitive) for matching field names.
                            If not provided, all available fields will be returned.

        Example:

        >>> mv.get_fields()
        >>> mv.get_fields("uniprot")
        >>> mv.get_fields("refseq")
        >>> mv.get_fields("kegg")

        .. Hint:: This is useful to find out the field names you need to pass to **fields** parameter of other methods.
        '''
}

for (_name, _docstring) in DOCSTRINGS.items():
    _func = getattr(MyGeneInfo, _name, None)
    if _func:
        _func.__doc__ = _docstring
