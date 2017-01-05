# -*- coding: utf-8 -*-

"""Determine more specific platform information than that which is available
with :func:`distutils.util.get_platform`.
"""

from __future__ import absolute_import

import distutils.util

from lionshead import linux, util


__version__ = '0.1'


def get_specific_platform():
    """Get the specific platform in a Pythonic representation. The return value is
    a 4-namedtuple with members:

    * :attr:`dist` - OS distribution (string)
    * :attr:`major_vers` - Distribution major version (string)
    * :attr:`full_vers` - Distribution full version (string)
    * :attr:`stability` - Stability (``stable`` or ``unstable``)

    Strings are not "sanitized" to remove characters considered invalid in
    platform strings such as in :func:`distutils.util.get_platform`.

    If the specific platform cannot be determined, ``None`` is returned.
    """
    base = distutils.util.get_platform().split('-')[0]
    if base == 'linux':
        return linux.get_specific_platform()
    return None


def get_specific_platform_string():
    """Returns the specific platform as a normalized string.
    """
    plat = get_specific_platform()
    if not plat:
        return str(None)
    if plat.major_vers == plat.full_vers:
        r = (plat.dist, plat.major_vers)
    else:
        r = (plat.dist, plat.major_vers, plat.full_vers)
    return '-'.join( [ util.normalize_name(e) for e in r ] )


def get_platform_stability_string():
    """Returns the platform's stability as a string.
    """
    plat = get_specific_platform()
    if not plat:
        return str(None)
    return plat.stability
