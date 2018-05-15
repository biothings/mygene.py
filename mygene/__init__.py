'''
Python Client for MyGene.Info services
'''
from biothings_client import get_client

class MyGeneInfo(get_client('gene', instance=False)):
    pass
