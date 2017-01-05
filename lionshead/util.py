# -*- coding: utf-8 -*-
from __future__ import absolute_import

import string
import sys
import unicodedata
from collections import namedtuple


spectuple = namedtuple('SpecificPlatform', ['dist',
                                            'major_vers',
                                            'full_vers',
                                            'stability'])


def normalize_name(s):
    """In Python 2, replaces all non-alphanumeric characters with ``_``. In
    Python 3, uses the `unicode identifiers rules
    <https://docs.python.org/3/reference/lexical_analysis.html#identifiers>`_
    to determine which characters to replace.

    :type s: str
    :param s: normalize 

    Returns a string.
    """
    if sys.version_info < (3, 0):
        valid = lambda x: x in string.ascii_letters + string.digits
    else:
        valid = lambda x: unicodedata.category(x) in ('Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Mn', 'Mc', 'Nd', 'Pc')
    s = list(s.lower())
    for i, c in enumerate(s):
        s[i:i+1] = c if valid(c) else '_'
    return ''.join(s)
