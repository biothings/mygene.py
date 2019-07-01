'''
Python Client for MyGene.Info services
'''
from biothings_client import alwayslist, get_client

__version__ = '3.1.0'


class MyGeneInfo(get_client('gene', instance=False)):

    def __init__(self):
        super(MyGeneInfo, self).__init__()
        self.default_user_agent += ' mygene.py/' + __version__

