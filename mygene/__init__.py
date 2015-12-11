'''
Python Client for MyGene.Info services
'''
from __future__ import print_function
import sys
import time
from itertools import islice
from collections import Iterable

import requests

try:
    from pandas import DataFrame
    df_avail = True
except:
    df_avail = False

__version__ = '2.3.0'

if sys.version_info[0] == 3:
    str_types = str
else:
    str_types = (str, unicode)


class ScanError(Exception):
    # for errors in scan search type
    pass


def alwayslist(value):
    '''If input value if not a list/tuple type, return it as a single value list.

    Example:

    >>> x = 'abc'
    >>> for xx in alwayslist(x):
    ...     print xx
    >>> x = ['abc', 'def']
    >>> for xx in alwayslist(x):
    ...     print xx

    '''
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


def safe_str(s, encoding='utf-8'):
    '''if input is an unicode string, do proper encoding.'''
    try:
        _s = str(s)
    except UnicodeEncodeError:
        _s = s.encode(encoding)
    return _s


def list_itemcnt(list):
    '''Return number of occurrence for each type of item in the list.'''
    x = {}
    for item in list:
        if item in x:
            x[item] += 1
        else:
            x[item] = 1
    return [(i, x[i]) for i in x]


def iter_n(iterable, n, with_cnt=False):
    '''
    Iterate an iterator by chunks (of n)
    if with_cnt is True, return (chunk, cnt) each time
    '''
    it = iter(iterable)
    if with_cnt:
        cnt = 0
    while True:
        chunk = tuple(islice(it, n))
        if not chunk:
            return
        if with_cnt:
            cnt += len(chunk)
            yield (chunk, cnt)
        else:
            yield chunk


class MyGeneInfo():
    '''This is the client for MyGene.info web services.
    Example:

        >>> mg = MyGeneInfo()

    '''
    def __init__(self, url='http://mygene.info/v2'):
        self.url = url
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.max_query = 1000
        # delay and step attributes are for batch queries.
        self.delay = 1
        self.step = 1000
        # raise requests.exceptions.HTTPError for status_code > 400
        #   but not for 404 on getgene
        #   set to False to surpress the exceptions.
        self.raise_for_status = True

    def _as_dataframe(self, gene_obj, df_index=True):
        """
        converts gene object to DataFrame (pandas)
        """
        if not df_avail:
            print("Error: pandas module must be installed for as_dataframe option.")
            return

        if 'hits' in gene_obj:
            df = DataFrame.from_dict(gene_obj['hits'])
        else:
            df = DataFrame.from_dict(gene_obj)
        if df_index:
            df = df.set_index('query')
        return df

    def _get(self, url, params={}, none_on_404=False):
        debug = params.pop('debug', False)
        return_raw = params.pop('return_raw', False)
        headers = {'user-agent': "Python-requests_mygene.py/%s (gzip)" % requests.__version__}
        res = requests.get(url, params=params, headers=headers)
        if debug:
            return res
        if none_on_404 and res.status_code == 404:
            return None
        if self.raise_for_status:
            # raise requests.exceptions.HTTPError if not 200
            res.raise_for_status()
        if return_raw:
            return res.text
        else:
            return res.json()

    def _post(self, url, params):
        return_raw = params.pop('return_raw', False)
        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'user-agent': "Python-requests_mygene.py/%s (gzip)" % requests.__version__}
        res = requests.post(url, data=params, headers=headers)
        if self.raise_for_status:
            # raise requests.exceptions.HTTPError if not 200
            res.raise_for_status()
        if return_raw:
            return res
        else:
            return res.json()

    def _is_entrez_id(self, id):
        try:
            int(id)
            return True
        except:
            return False

    def _format_list(self, a_list, sep=','):
        if isinstance(a_list, (list, tuple)):
            _out = sep.join([safe_str(x) for x in a_list])
        else:
            _out = a_list     # a_list is already a comma separated string
        return _out

    def _repeated_query_old(self, query_fn, query_li, verbose=True, **fn_kwargs):
        step = min(self.step, self.max_query)
        if len(query_li) <= step:
            # No need to do series of batch queries, turn off verbose output
            verbose = False
        for i in range(0, len(query_li), step):
            is_last_loop = i+step >= len(query_li)
            if verbose:
                print("querying {0}-{1}...".format(i+1, min(i+step, len(query_li))), end="")
            query_result = query_fn(query_li[i:i+step], **fn_kwargs)

            yield query_result

            if verbose:
                print("done.")
            if not is_last_loop and self.delay:
                time.sleep(self.delay)

    def _repeated_query(self, query_fn, query_li, verbose=True, **fn_kwargs):
        '''run query_fn for input query_li in a batch (self.step).
           return a generator of query_result in each batch.
           input query_li can be a list/tuple/iterable
        '''
        step = min(self.step, self.max_query)
        i = 0
        for batch, cnt in iter_n(query_li, step, with_cnt=True):
            if verbose:
                print("querying {0}-{1}...".format(i+1, cnt), end="")
            i = cnt
            query_result = query_fn(batch, **fn_kwargs)
            yield query_result
            if verbose:
                print("done.")
            if self.delay:
                time.sleep(self.delay)

    @property
    def metadata(self):
        '''Return a dictionary of MyGene.info metadata.

        Example:

        >>> metadata = mg.metadata

        '''
        _url = self.url+'/metadata'
        return self._get(_url)

    def get_fields(self, search_term=None):
        ''' Wrapper for http://mygene.info/v2/metadata/fields
            **search_term** is a case insensitive string to search for in available field names.
            If not provided, all available fields will be returned.
        Example:
        >>> mv.get_fields()
        >>> mv.get_fields("uniprot")
        >>> mv.get_fields("refseq")
        >>> mv.get_fields("kegg")
        .. Hint:: This is useful to find out the field names you need to pass to **fields** parameter of other methods.
        '''
        _url = self.url + '/metadata/fields'
        these_fields = self._get(_url)
        if search_term:
            ret = dict([(k, v) for (k, v) in these_fields.items() if search_term.lower() in k.lower()])
        else:
            ret = these_fields
        for (k, v) in ret.items():
            # Get rid of the notes column information
            if "notes" in v:
                del v['notes']
        return ret

    def getgene(self, geneid, fields='symbol,name,taxid,entrezgene', **kwargs):
        '''Return the gene object for the give geneid.
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

        :ref: http://mygene.info/doc/annotation_service.html for available
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
        '''
        if fields:
            kwargs['fields'] = self._format_list(fields)
        if 'filter' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['filter'])
        _url = self.url + '/gene/' + str(geneid)
        return self._get(_url, kwargs, none_on_404=True)

    def _getgenes_inner(self, geneids, **kwargs):
        _kwargs = {'ids': self._format_list(geneids)}
        _kwargs.update(kwargs)
        _url = self.url + '/gene'
        return self._post(_url, _kwargs)

    def getgenes(self, geneids, fields='symbol,name,taxid,entrezgene', **kwargs):
        '''Return the list of gene objects for the given list of geneids.
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
        '''
        if isinstance(geneids, str_types):
            geneids = geneids.split(',')
        if (not (isinstance(geneids, (list, tuple, Iterable)))):
            raise ValueError('input "geneids" must be a list, tuple or iterable.')

        if fields:
            kwargs['fields'] = self._format_list(fields)
        if 'filter' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['filter'])
        verbose = kwargs.pop('verbose', True)
        as_dataframe = kwargs.pop('as_dataframe', False)
        if as_dataframe:
            df_index = kwargs.pop('df_index', True)
        return_raw = kwargs.get('return_raw', False)
        if return_raw:
            as_dataframe = False

        query_fn = lambda geneids: self._getgenes_inner(geneids, **kwargs)
        out = []
        for hits in self._repeated_query(query_fn, geneids, verbose=verbose):
            if return_raw:
                out.append(hits)   # hits is the raw response text
            else:
                out.extend(hits)
        if return_raw and len(out) == 1:
            out = out[0]
        if as_dataframe:
            out = self._as_dataframe(out, df_index)
        return out

    def query(self, q, **kwargs):
        '''Return  the query result.
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

        '''
        as_dataframe = kwargs.pop('as_dataframe', False)
        kwargs.update({'q': q})
        fetch_all = kwargs.get('fetch_all')
        if fetch_all in [True, 1]:
            return self._fetch_all(**kwargs)
        _url = self.url + '/query'
        out = self._get(_url, kwargs)
        if as_dataframe:
            out = self._as_dataframe(out, False)
        return out

    def _fetch_all(self, **kwargs):
        ''' Function that returns a generator to query results.  Assumes that 'q' is in kwargs.'''
        # get the total number of hits and start the scroll_id
        _url = self.url + '/query'
        res = self._get(_url, kwargs)
        try:
            scroll_id = res['_scroll_id']
            total_hits = int(res['total'])
        except KeyError:
            raise ScanError("Unable to open scroll.")
        if total_hits == 0:
            raise StopIteration
        kwargs.pop('q', None)
        kwargs.pop('fetch_all', None)
        print("Fetching {0} object(s)...".format(total_hits))
        while True:
            # get next scroll results
            kwargs.update({'scroll_id': scroll_id})
            out = self._get(_url, kwargs)
            if 'error' in out:
                break
            if '_warning' in out:
                print(out['_warning'])
            scroll_id = out.get('_scroll_id')
            for hit in out['hits']:
                yield hit

    def _querymany_inner(self, qterms, **kwargs):
        _kwargs = {'q': self._format_list(qterms)}
        _kwargs.update(kwargs)
        _url = self.url + '/query'
        return self._post(_url, _kwargs)

    def querymany(self, qterms, scopes=None, **kwargs):
        '''Return the batch query result.
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

        '''
        if isinstance(qterms, str_types):
            qterms = qterms.split(',')
        if (not (isinstance(qterms, (list, tuple, Iterable)))):
            raise ValueError('input "qterms" must be a list, tuple or iterable.')

        if scopes:
            kwargs['scopes'] = self._format_list(scopes)
        if 'scope' in kwargs:
            # allow scope for back-compatibility
            kwargs['scopes'] = self._format_list(kwargs['scope'])
        if 'fields' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['fields'])
        if 'species' in kwargs:
            kwargs['species'] = self._format_list(kwargs['species'])
        returnall = kwargs.pop('returnall', False)
        verbose = kwargs.pop('verbose', True)
        as_dataframe = kwargs.pop('as_dataframe', False)
        if as_dataframe:
            df_index = kwargs.pop('df_index', True)
        return_raw = kwargs.get('return_raw', False)
        if return_raw:
            as_dataframe = False

        out = []
        li_missing = []
        li_dup = []
        li_query = []
        query_fn = lambda qterms: self._querymany_inner(qterms, **kwargs)
        for hits in self._repeated_query(query_fn, qterms, verbose=verbose):
            if return_raw:
                out.append(hits)   # hits is the raw response text
            else:
                out.extend(hits)
                for hit in hits:
                    if hit.get('notfound', False):
                        li_missing.append(hit['query'])
                    else:
                        li_query.append(hit['query'])

        if verbose:
            print("Finished.")
        if return_raw:
            if len(out) == 1:
                out = out[0]
            return out
        if as_dataframe:
            out = self._as_dataframe(out, df_index)

        # check dup hits
        if li_query:
            li_dup = [(query, cnt) for query, cnt in list_itemcnt(li_query) if cnt > 1]
        del li_query

        if verbose:
            if li_dup:
                print("{0} input query terms found dup hits:".format(len(li_dup)))
                print("\t"+str(li_dup)[:100])
            if li_missing:
                print("{0} input query terms found no hit:".format(len(li_missing)))
                print("\t"+str(li_missing)[:100])
        if returnall:
            return {'out': out, 'dup': li_dup, 'missing': li_missing}
        else:
            if verbose and (li_dup or li_missing):
                print('Pass "returnall=True" to return complete lists of duplicate or missing query terms.')
            return out

    def findgenes(self, id_li, **kwargs):
        '''.. deprecated:: 2.0.0

        Use :py:meth:`querymany` instead. It's kept here as an alias of :py:meth:`querymany` method.
        '''
        import warnings
        warnings.warn('Deprecated! Currently an alias of "querymany" method. Use "querymany" method directly.', DeprecationWarning)
        return self.querymany(id_li, **kwargs)
