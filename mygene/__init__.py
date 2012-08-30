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


class MyGeneInfo():
    def __init__(self, url='http://mygene.info'):
        self.url = url
        if self.url[-1] == '/':
            self.url = self.url[:-1]
        self.h = httplib2.Http()
        self.max_query=1000

        #check http://mygene.info/metadata for the most updated species list
        self.taxid_d = {'human': 9606,
                        'mouse': 10090,
                        'rat':   10116,
                        'fruitfly': 7227,
                        'nematode':   6239,
                        'zebrafish':   7955,
                        'thale-cress':   3702,
                        'frog':   8364,
                        'pig': 9823,
                       }

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
            _out = sep.join([str(x) for x in a_list])
        else:
            _out = a_list     # a_list is already a comma separated string
        return _out

    def _repeated_query(self, query_fn, query_li, delay=1, step=1000, verbose=True):
        step = min(step, self.max_query)
        for i in range(0, len(query_li), step):
            is_last_loop = i+step >= len(query_li)
            if verbose:
                print "querying %d-%d..." % (i+1, min(i+step, len(query_li))),
            query_result = query_fn(query_li[i:i+step])

            yield query_result

            if verbose:
                print
            if not is_last_loop and delay:
                time.sleep(delay)

    @property
    def metadata(self):
        _url = self.url+'/metadata'
        return self._get(_url)

    def getgene(self, geneid, filter='symbol,name', **kwargs):
        '''Return the gene object for the give geneid.
           This is a wrapper for GET query of "/gene/<geneid>" service.
             @param geneid: entrez/ensembl gene id
             @param filter: fields to return, a list of a comma-sep string
                            if filter==None, full gene object is returned.
           Refer to http://mygene.info/doc/anno_service for available filters.
        '''
        if filter: kwargs['filter'] = self._format_list(filter)
        _url = self.url + '/gene/' + str(geneid)
        return self._get(_url, kwargs)

    def getgenes(self, geneids, filter='symbol,name', **kwargs):
        '''Return the list of gene object for the given list of geneids.
           This is a wrapper for POST query of "/gene" service.
             @param geneids: a list or comm-sep entrez/ensembl gene ids
             @param filter: fields to return, a list of a comma-sep string
                            if filter==None, full gene object is returned.
          Refer to http://mygene.info/doc/anno_service for available filters.
        '''
        kwargs.update({'ids': self._format_list(geneids)})
        if filter: kwargs['filter'] = self._format_list(filter)
        _url = self.url + '/gene'
        return self._post(_url, kwargs)

    def query(self, q, limit=None, skip=None, sort=None, **kwargs):
        '''Return  the query result.
           This is a wrapper for GET query of "/query?q=<query>" service.
           Refer to http://mygene.info/doc/query_service for query syntax.
            @param limit:   the maximum number of results to return (with a cap
                              of 1000 at the moment)
            @param skip:    the number of results to skip
            @param sort:    the comma-separated fields to sort on. Prefix with / for
                             ascending order and \ for descending order (default as
                             ascending)
        '''
        kwargs.update({'q': q})
        if limit: kwargs['limit'] = limit
        if skip: kwargs['skip'] = skip
        if sort: kwargs['sort'] = sort
        _url = self.url + '/query'
        return self._get(_url, kwargs)

    def querymany(self, qterms, scope=None, **kwargs):
        '''Return the batch query result.
           This is a wrapper for POST query of "/query" service.
           Refer to http://mygene.info/doc/query_service for query syntax.

            @param qterms: either a list of query terms or a string with comma-separated
                            query terms.
            @param scope:  type of types of identifiers, either a list or a comma-separated fields to specify type of
                           input qterms, e.g. "entrezgene", "entrezgene,symbol", ["ensemblgene", "symbol"]
                           refer to "http://mygene.info/doc/query_service#available_fields" for full list
                           of fields.


        '''
        kwargs.update({'q': self._format_list(qterms)})
        if scope:
            kwargs['scope'] = self._format_list(scope)
        _url = self.url + '/query'
        #return kwargs
        return self._post(_url, kwargs)

    def findgenes(self, id_li, scope, species='all', entrezonly=False, delay=1,
                   step=1000, raw=False, returnall=False):
        '''return matched entrez gene ids for input id_li,
           parameter "scope" specifies the type of ids,
            which can be either a string for a single type
            or a tuple of multiple type strings.
           This is a wrapper for POST query of "/query" service.
            @param id_li:       a list of identifers
            @param scope:       type of types of identifiers, either a list or a comma-separated fields
                                to specify type of input qterms, e.g. "entrezgene", "entrezgene,symbol",
                                ["ensemblgene", "symbol"]
                                refer to "http://mygene.info/doc/query_service#available_fields" for full
                                list of fields.
            @param species:     "all" or one of "human", "mouse", "rat", etc.
                                 if input is an integer, it's interpreted as a taxonomy id (taxid).
                                 refer to http://mygene.info/metadata for all supported species and taxids.
                                 if input species names or taxids are not supported, it will be ignored and
                                 use default "all".

            @param entrezonly:  if True, return only matching entrez gene, otherwise, including matching
                                 Ensemble-only genes (those have no matching entrez genes).
            @param raw:         if True, return a list of raw query results
            @param returnall:   if True, return a dict of all related data.
        '''
        if type(scope) not in [types.ListType, types.TupleType]:
            scope = [scope]

        if type(species) is types.IntType:
            #so it is a taxid
            taxid = species if species in self.taxid_d.values() else None
        else:
            #otherwise, treat is as a species name
            taxid = self.taxid_d.get(species, None)

        out = []
        res = {}
        li_dup = []
        li_missing = []
        query_fn = lambda ids: self.querymany(qterms=ids, scope=scope)
        for hits in self._repeated_query(query_fn, id_li, delay=delay, step=step):
            if raw:
                out.extend(hits['rows'])
            else:
                rows = [(g['key'][0], g['id'], g.get('symbol',''), g.get('name','')) \
                         for g in hits['rows'] \
                         if (taxid is None or g['taxid'] == taxid) and \
                            (entrezonly is False or self._is_entrez_id(g['id'])) ]
                res.update(list2dict(rows, 0))
        if not raw:
            for id in id_li:
                rows = res.get(safe_str(id).lower(), None)
                if rows:
                    if type(rows) is types.ListType:
                        out.append((id,) + tuple(['//'.join([str(row[i]) for row in rows]) for i in range(len(rows[0]))]) )
                        li_dup.append(id)
                    else:
                        out.append((id,)+rows)
                else:
                    out.append((id, ) + ('',)*3)
                    li_missing.append(id)
        print "Finished."
        if len(li_dup)>0:
            print "%d input ids found dup hits:" % len(li_dup)
            print "\t"+str(li_dup)[:100]
        if len(li_missing)>0:
            print "%d input ids found no hit:" % len(li_missing)
            print "\t"+str(li_missing)[:100]
        if returnall:
            return {'out': out, 'res':res, 'dup':li_dup, 'missing':li_missing}
        else:
            return out




