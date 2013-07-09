'''
Python Client for MyGene.Info services
'''
import types
import time
import urllib
import httplib2
try:
    import simplejson as json
except:
    import json


def list2dict(list,keyitem,alwayslist=False):
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
    dict={}
    for x in list:
        if type(keyitem)==type(0):      #single item as key
            key=x[keyitem]
            value=tuple(x[:keyitem]+x[keyitem+1:])
        else:                           #
            key=tuple([x[i] for i in keyitem])
            value=tuple([x[i] for i in range(len(list)) if i not in keyitem])
        if len(value) == 1:      #single value
            value=value[0]
        if not dict.has_key(key):
            if alwayslist:
                dict[key] = [value,]
            else:
                dict[key]=value
        else:
            current_value=dict[key]
            if type(current_value) != type([]):
                current_value=[current_value,]
            current_value.append(value)
            dict[key]=current_value
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
    x={}
    for item in list:
        if x.has_key(item):
            x[item]+=1
        else:
            x[item]=1
    return [(i,x[i]) for i in x]


class MyGeneInfo():
    def __init__(self, url='http://mygene.info/v2'):
        self.url = url
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.h = httplib2.Http()
        self.max_query=1000

    def _get(self, url, params={}):
        debug = params.pop('debug', False)
        return_raw = params.pop('return_raw', False)
        if params:
            _url = url + '?' + urllib.urlencode(params)
        else:
            _url = url
        res, con = self.h.request(_url)
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
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        res, con = self.h.request(url, 'POST', body=urllib.urlencode(params), headers=headers)
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
        if type(a_list) in (types.ListType, types.TupleType):
            _out = sep.join([safe_str(x) for x in a_list])
        else:
            _out = a_list     # a_list is already a comma separated string
        return _out

    def _repeated_query(self, query_fn, query_li, delay=1, step=1000, verbose=True, **fn_kwargs):
        step = min(step, self.max_query)
        for i in range(0, len(query_li), step):
            is_last_loop = i+step >= len(query_li)
            if verbose:
                print "querying %d-%d..." % (i+1, min(i+step, len(query_li))),
            query_result = query_fn(query_li[i:i+step], **fn_kwargs)

            yield query_result

            if verbose:
                print "done."
            if not is_last_loop and delay:
                time.sleep(delay)

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
        if fields: kwargs['fields'] = self._format_list(fields)
        if 'filter' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['filter'])
        _url = self.url + '/gene/' + str(geneid)
        return self._get(_url, kwargs)

    def getgenes(self, geneids, fields='symbol,name,taxid,entrezgene', **kwargs):
        '''Return the list of gene object for the given list of geneids.
           This is a wrapper for POST query of "/gene" service.
             @param geneids: a list or comm-sep entrez/ensembl gene ids
             @param fields: fields to return, a list of a comma-sep string
                            if fields=="all", all available fields are returned.
             @param species: optionally, you can pass comma-separated species names
                              or taxonomy ids
             @param filter: alias for fields
          Ref: http://mygene.info/doc/annotation_service.html
        '''
        kwargs.update({'ids': self._format_list(geneids)})
        if fields: kwargs['fields'] = self._format_list(fields)
        if 'filter' in kwargs:
            kwargs['fields'] = self._format_list(kwargs['filter'])
        _url = self.url + '/gene'
        return self._post(_url, kwargs)

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

            Ref: http://mygene.info/doc/query_service.html
        '''
        kwargs.update({'q': q})
        _url = self.url + '/query'
        return self._get(_url, kwargs)

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
            @param entrezonly:  if True, return only matching entrez gene, otherwise, including matching
                                 Ensemble-only genes (those have no matching entrez genes).

            @delay
            @step
            #@param raw:         if True, return a list of raw query results
            @param returnall:   if True, return a dict of all related data, including dup. and missing qterms
            #@asiter:            if True, return a iterator instead of a list
            @verbose            if True (default), print out infomation about dup and missing qterms


            Ref: http://mygene.info/doc/query_service.html

        '''
        if type(qterms) in types.StringTypes:
            qterms = qterms.split(',')
        if (not (type(qterms) in (types.ListType, types.TupleType) and len(qterms) > 0)):
            raise ValueError('input "qterms" must be non-empty list or tuple.')

        if scopes:
            kwargs['scopes'] = self._format_list(scopes)
        if 'scope' in kwargs:
            #allow scope for back-compatibility
            kwargs['scopes'] = self._format_list(kwargs['scope'])
        if 'species' in kwargs:
            kwargs['species'] = self._format_list(kwargs['species'])
        raw = kwargs.pop('raw', False)
        returnall = kwargs.pop('returnall', False)
        delay = kwargs.pop('delay', 1)
        step = kwargs.pop('step', 1000)
        verbose = kwargs.pop('verbose', True)

        out = []
        li_missing = []
        li_dup = []
        li_query = []
        query_fn = lambda qterms: self._querymany_inner(qterms, **kwargs)
        for hits in self._repeated_query(query_fn, qterms, delay=delay, step=step, verbose=verbose):
            out.extend(hits)
            for hit in hits:
                if hit.get('notfound', False):
                    li_missing.append(hit['query'])
                else:
                    li_query.append(hit['query'])
        if verbose:
            print "Finished."
        #check dup hits
        if li_query:
            li_dup = [(query, cnt) for query, cnt in list_itemcnt(li_query) if cnt > 1]
        del li_query

        if verbose:
            if li_dup:
                print "%d input query terms found dup hits:" % len(li_dup)
                print "\t"+str(li_dup)[:100]
            if li_missing:
                print "%d input query terms found no hit:" % len(li_missing)
                print "\t"+str(li_missing)[:100]
        if returnall:
            return {'out': out, 'dup':li_dup, 'missing':li_missing}
        else:
            if verbose and (li_dup or li_missing):
                print 'Pass "returnall=True" to return complete lists of duplicate or missing query terms.'
            return out


    def findgenes(self, id_li, **kwargs):
        ''' Deprecated! It's kept here as an alias of "querymany" method.'''
        return self.querymany(id_li, **kwargs)

