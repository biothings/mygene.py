import unittest
import mygene

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.mg = mygene.MyGeneInfo()

    def test_metadata(self):
        meta = self.mg.metadata
        self.assertTrue("TOTAL_GENE_DOC" in meta)

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
        qres = self.mg.query('cdk2', limit=5)
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 5)
        
    def test_query_reporter(self):
        qres = self.mg.query('reporter:1000_at')
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 1)
        self.assertEqual(qres['rows'][0]['id'], '5595')
        
    def test_query_symbol(self):
        qres = self.mg.query('symbol:cdk2 AND species:human')
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 1)
        self.assertEqual(qres['rows'][0]['id'], '1017')

    
    def test_querymany(self):
        qres = self.mg.querymany([1017, '695'])
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 2)

        qres = self.mg.querymany("1017,695")
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 2)
    
    def test_querymany_with_scope(self):
        qres = self.mg.querymany([1017, '695'], scope='entrezgene')
        self.assertTrue('rows' in qres)
        self.assertEqual(len(qres['rows']), 2)
        
        qres = self.mg.querymany([1017, 'BTK'], scope='entrezgene,symbol')
        self.assertTrue('rows' in qres)
        self.assertTrue(len(qres['rows'])>=2)


    def test_findgenes(self):
        qres = self.mg.findgenes([1017, '695'], scope='entrezgene', species='human')
        self.assertEqual(len(qres), 2)
        
        qres = self.mg.findgenes([1017, '695'], scope='entrezgene', species=9606)
        self.assertEqual(len(qres), 2)
        
        qres = self.mg.findgenes([1017, 'CDK2'], scope='entrezgene,symbol', species=9606)
        self.assertEqual(len(qres), 2)
        
        qres = self.mg.findgenes([1017, '695', 'NA_TEST'], scope='entrezgene', species=9606)
        self.assertEqual(len(qres), 3)
        self.assertEqual(qres[2], ('NA_TEST', '', '', ''))
        
        qres = self.mg.findgenes([1017, '695'], scope='entrezgene', species=9606, raw=True)
        self.assertEqual(len(qres), 2)


if __name__ == '__main__':
    unittest.main()