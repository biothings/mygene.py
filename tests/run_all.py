
import doctest
import test0
doctest.testmod(test0, optionflags=doctest.NORMALIZE_WHITESPACE |
                                   doctest.ELLIPSIS |
                                   doctest.REPORT_ONLY_FIRST_FAILURE
                                   )

