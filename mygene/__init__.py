'''
Python Client for MyGene.Info services
'''
from biothings_client import get_client, alwayslist

__version__ = '3.1.0'

class MyGeneInfo(get_client('gene', instance=False)):
    pass
