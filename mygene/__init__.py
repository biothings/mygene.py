'''
Python Client for MyGene.Info services
'''
from __future__ import print_function
import sys
import time
import httplib2
import json
try:
    from pandas import DataFrame
    df_avail = True
except:
    df_avail = False

__version__ = '2.2.0'

if sys.version_info[0] == 3:
    str_types = str
    from urllib.parse import urlencode
else:
    str_types = (str, unicode)
    from urllib import urlencode


def alwayslist(value):
    """If input value if not a list/tuple type, return it as a single value list."""
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


def list2dict(list, keyitem, alwayslist=False):
    '''Return a dictionary with specified keyitem as key, others as values.
       keyitem can be an index or a sequence of indexes.
       For example: li=[['A','a',1],
                        ['B','a',2],
                        ['A','b',3]]
                    list2dict(li,0)---> {'A':[('a',1),('b',3)],
                                         'B':('a',2)}
       if alwayslist is True, values are always a list even there is only one item in it.
                    list2dict(li,0,True)---> {'A':[('a',1),('b',3)],
                                              'B':[('a',2),]}
    '''
    dict = {}
    for x in list:
        if isinstance(keyitem, int):      # single item as key
            key = x[keyitem]
            value = tuple(x[:keyitem] + x[keyitem+1:])
        else:
            key = tuple([x[i] for i in keyitem])
            value = tuple([x[i] for i in range(len(list)) if i not in keyitem])
        if len(value) == 1:      # single value
            value = value[0]
        if key not in dict:
            if alwayslist:
                dict[key] = [value]
            else:
                dict[key] = value
        else:
            current_value = dict[key]
            if not isinstance(current_value, list):
                current_value = [current_value]
            current_value.append(value)
            dict[key] = current_value
    return dict


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


class MyGeneInfo():
    def __init__(self, url='http://mygene.info/v2'):
        self.url = url
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.h = httplib2.Http()
        self.max_query = 1000
        # delay and step attributes are for batch queries.
        self.delay = 1
        self.step = 1000

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

    def _get(self, url, params={}):
        debug = params.pop('debug', False)
        return_raw = params.pop('return_raw', False)
        headers = {'user-agent': "Python-httplib2_mygene.py/%s (gzip)" % httplib2.__version__}
        if params:
            _url = url + '?' + urlencode(params)
        else:
            _url = url
        res, con = self.h.request(_url, headers=headers)
        con = con.decode("utf8")  # required in python3
        if debug:
            return _url, res, con
        assert res.status == 200, (_url, res, con)
        if return_raw:
            return con
        else:
            return json.loads(con)

    def _post(self, url, params):
        debug = params.pop('debug', False)
        return_raw = params.pop('return_raw', False)
        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'user-agent': "Python-httplib2_mygene.py/%s (gzip)" % httplib2.__version__}
        res, con = self.h.request(url, 'POST', body=urlencode(params), headers=headers)
        con = con.decode("utf8")  # required in python3
        if debug:
            return url, res, con
        assert res.status == 200, (url, res, con)
        if return_raw:
            return con
        else:
            return json.loads(con)

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

    def _repeated_query(self, query_fn, query_li, verbose=True, **fn_kwargs):
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

    @property
    def metadata(self):
        _url = self.url+'/metadata'
        return self._get(_url)

    def getgene(self, geneid, fields='symbol,name,taxid,entrezgene', **kwargs):
        '''Return the gene object for the give geneid.
           This is a wrapper for GET query of "/gene/<geneid>" service.
             @param geneid: entrez/ensembl gene id
             @param fields: fields to return, a list of a comma-sep string
                            if fields=="all", all available fields are returned.
             @param species: optionally, you can pass comma-separated species names
                              or taxonomy ids
             @param filter: alias for fields

           Ref: http://mygene.info/doc/annotation_service.html
        '''
        if fields:
            kwargs['fields'] = self._format_list(fields)
        if 'filter' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['filter'])
        _url = self.url + '/gene/' + str(geneid)
        return self._get(_url, kwargs)

    def _getgenes_inner(self, geneids, **kwargs):
        _kwargs = {'ids': self._format_list(geneids)}
        _kwargs.update(kwargs)
        _url = self.url + '/gene'
        return self._post(_url, _kwargs)

    def getgenes(self, geneids, fields='symbol,name,taxid,entrezgene', **kwargs):
        '''Return the list of gene object for the given list of geneids.
           This is a wrapper for POST query of "/gene" service.
             @param geneids: a list or comm-sep entrez/ensembl gene ids
             @param fields: fields to return, a list of a comma-sep string
                            if fields=="all", all available fields are returned.
             @param species: optionally, you can pass comma-separated species names
                              or taxonomy ids
             @param filter: alias for fields
             @param as_dataframe: if True, return object as dataframe.
             @param df_index: if True (default), index dataframe by 'query', else index
                    by number. Only applicable if as_dataframe=True.

          Ref: http://mygene.info/doc/annotation_service.html
        '''
        if isinstance(geneids, str_types):
            geneids = geneids.split(',')
        if (not (isinstance(geneids, (list, tuple)) and len(geneids) > 0)):
            raise ValueError('input "geneids" must be non-empty list or tuple.')
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
            @param fields: fields to return, a list of a comma-sep string
                            if fields=="all", all available fields are returned.
            @param species: optionally, you can pass comma-separated species names
                              or taxonomy ids. Default: human,mouse,rat.
            @param size:   the maximum number of results to return (with a cap
                              of 1000 at the moment). Default: 10.
            @param skip:    the number of results to skip. Default: 0.
            @param sort:    Prefix with "-" for descending order, otherwise in ascending order.
                            Default: sort by matching scores in decending order.
            @param entrezonly: if True, return only matching entrez genes, otherwise, including matching
                                 Ensemble-only genes (those have no matching entrez genes).
            @param as_dataframe: if True, return object as dataframe.
            @param df_index: if True (default), index dataframe by 'query', else index
                   by number. Only applicable if as_dataframe=True.

            Ref: http://mygene.info/doc/query_service.html
        '''
        as_dataframe = kwargs.pop('as_dataframe', False)
        kwargs.update({'q': q})
        _url = self.url + '/query'
        out = self._get(_url, kwargs)
        if as_dataframe:
            out = self._as_dataframe(out, False)
        return out

    def _querymany_inner(self, qterms, **kwargs):
        _kwargs = {'q': self._format_list(qterms)}
        _kwargs.update(kwargs)
        _url = self.url + '/query'
        return self._post(_url, _kwargs)

    def querymany(self, qterms, scopes=None, **kwargs):
        '''Return the batch query result.
           This is a wrapper for POST query of "/query" service.

            @param qterms: a list of query terms, or a string of comma-separated query terms.
            @param scopes:  type of types of identifiers, either a list or a comma-separated fields to specify type of
                           input qterms, e.g. "entrezgene", "entrezgene,symbol", ["ensemblgene", "symbol"]
                           refer to "http://mygene.info/doc/query_service.html#available_fields" for full list
                           of fields.
            @param fields: fields to return, a list of a comma-sep string
                            if fields=="all", all available fields are returned.
            @param species: optionally, you can pass comma-separated species names
                              or taxonomy ids. Default: human,mouse,rat.
            @param entrezonly:  if True, return only matching entrez genes, otherwise, including matching
                                 Ensemble-only genes (those have no matching entrez genes).

            @param returnall:   if True, return a dict of all related data, including dup. and missing qterms
            @param verbose:     if True (default), print out infomation about dup and missing qterms
            @param as_dataframe: if True, return object as dataframe.
            Ref: http://mygene.info/doc/query_service.html
        '''
        if isinstance(qterms, str_types):
            qterms = qterms.split(',')
        if (not (isinstance(qterms, (list, tuple)) and len(qterms) > 0)):
            raise ValueError('input "qterms" must be non-empty list or tuple.')

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
        ''' Deprecated! It's kept here as an alias of "querymany" method.'''
        import warnings
        warnings.warn('Deprecated! Currently an alias of "querymany" method. Use "querymany" method directly.', DeprecationWarning)
        return self.querymany(id_li, **kwargs)
