import unittest
import sys
sys.path.insert(0, '..')
import mygene
print '"mygene {}" loaded from "{}"'.format(mygene.__version__, mygene.__file__)

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mg = mygene.MyGeneInfo()

    def test_metadata(self):
        meta = self.mg.metadata
        self.assertTrue("stats" in meta)
        self.assertTrue("total_genes" in meta['stats'])

    def test_getgene(self):
        g = self.mg.getgene("1017")
        self.assertEqual(g['_id'], "1017")
        self.assertEqual(g['symbol'], 'CDK2')

    def test_getgene_with_filter(self):
        g = self.mg.getgene("1017", "name,symbol,refseq")
        self.assertTrue('_id' in g)
        self.assertTrue('name' in g)
        self.assertTrue('symbol' in g)
        self.assertTrue('refseq' in g)

    def test_getgenes(self):
        g_li = self.mg.getgenes([1017,1018,'ENSG00000148795'])
        self.assertEqual(len(g_li), 3)
        self.assertEqual(g_li[0]['_id'], '1017')
        self.assertEqual(g_li[1]['_id'], '1018')
        self.assertEqual(g_li[2]['_id'], '1586')

    def test_query(self):
        qres = self.mg.query('cdk2', size=5)
        self.assertTrue('hits' in qres)
        self.assertEqual(len(qres['hits']), 5)

    def test_query_reporter(self):
        qres = self.mg.query('reporter:1000_at')
        self.assertTrue('hits' in qres)
        self.assertEqual(len(qres['hits']), 1)
        self.assertEqual(qres['hits'][0]['_id'], '5595')

    def test_query_symbol(self):
        qres = self.mg.query('symbol:cdk2', species='mouse')
        self.assertTrue('hits' in qres)
        self.assertEqual(len(qres['hits']), 1)
        self.assertEqual(qres['hits'][0]['_id'], '12566')


    def test_querymany(self):
        qres = self.mg.querymany([1017, '695'], verbose=False)
        self.assertEqual(len(qres), 2)

        qres = self.mg.querymany("1017,695", verbose=False)
        self.assertEqual(len(qres), 2)

    def test_querymany_with_scopes(self):
        qres = self.mg.querymany([1017, '695'], scopes='entrezgene', verbose=False)
        self.assertEqual(len(qres), 2)

        qres = self.mg.querymany([1017, 'BTK'], scopes='entrezgene,symbol', verbose=False)
        self.assertTrue(len(qres)>=2)


    def test_querymany_species(self):
        qres = self.mg.querymany([1017, '695'], scopes='entrezgene', species='human', verbose=False)
        self.assertEqual(len(qres), 2)

        qres = self.mg.findgenes([1017, '695'], scopes='entrezgene', species=9606, verbose=False)
        self.assertEqual(len(qres), 2)

        qres = self.mg.findgenes([1017, 'CDK2'], scopes='entrezgene,symbol', species=9606, verbose=False)
        self.assertEqual(len(qres), 2)

    def test_querymany_fields(self):
        qres1 = self.mg.findgenes([1017, 'CDK2'], scopes='entrezgene,symbol', fields=['uniprot', 'unigene'], species=9606, verbose=False)
        self.assertEqual(len(qres1), 2)

        qres2 = self.mg.findgenes([1017, 'CDK2'], scopes='entrezgene,symbol', fields='uniprot,unigene', species=9606, verbose=False)
        self.assertEqual(len(qres2), 2)

        self.assertEqual(qres1, qres2)

    def test_querymany_notfound(self):
        qres = self.mg.findgenes([1017, '695', 'NA_TEST'], scopes='entrezgene', species=9606)
        self.assertEqual(len(qres), 3)
        self.assertEqual(qres[2], {"query": 'NA_TEST', "notfound": True})


if __name__ == '__main__':
    unittest.main()
