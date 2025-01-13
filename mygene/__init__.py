"""
Python Client for MyGene.Info services
"""

from biothings_client import get_client

__version__ = "3.2.2"


# import alwayslist helper function here in case users
# still use "from mygene import alwayslist"


# *** NOTE ***
# Initially removed from biothings_client as nothing in our core
# code used. Appears it was used here for external usage. Moving
# here in case users still utilize it (Jan 13, 2025)
def alwayslist(value):
    """If input value if not a list/tuple type, return it as a single value list.

    Example:

    >>> x = 'abc'
    >>> for xx in alwayslist(x):
    ...     print xx
    >>> x = ['abc', 'def']
    >>> for xx in alwayslist(x):
    ...     print xx

    """
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


class MyGeneInfo(get_client("gene", instance=False)):

    def __init__(self):
        super(MyGeneInfo, self).__init__()
        self.default_user_agent += " mygene.py/" + __version__
