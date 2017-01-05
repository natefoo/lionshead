# -*- coding: utf-8 -*-

"""Detect specific platform on Linux.
"""

from __future__ import absolute_import

import os
import re
import shlex
import subprocess
import glob

from lionshead.util import spectuple


# These distributions do not produce rolling or unstable releases
STABLE_DISTRIBUTIONS = (
        'centos',
        'redhat',
        'sles',
        'ubuntu'
)


def _get_major_version(dist, version):
    """Given a Linux distribution and "full" version number, return only the
    "major" version number for that platform

    :param dist: Detected Linux distribution
    :param version: Detected version of the given distribution
    """
    if dist == 'ubuntu':
        version = '.'.join(version.split('.')[0:2])
    else:
        version = version.split('.')[0]
    return version


_opensuse_tumbleweed_version = re.compile('\d{8}$')

def _get_stability(dist, version):
    """Determine whether or not the ABI for the given distribution and verison
    can be considered stable.

    :param dist: Detected Linux distribution
    :param version: Detected version of the given distribution
    """
    stability = 'unstable'
    if dist in STABLE_DISTRIBUTIONS:
        stability = 'stable'
    elif dist == 'debian' and not version.endswith('/sid'):
        stability = 'stable'
    elif dist == 'opensuse' and not _opensuse_tumbleweed_version.match(version):
        stability = 'stable'
    return stability


def _parse_source_file(fname):
    with open(fname) as fh:
        return dict([line.split('=', 1) for line in shlex.split(fh.read())])


def _read_os_release():
    files = [ '/etc/os-release',
              '/usr/lib/os-release' ]

    osrel_file = None
    for osrel_file in files:
        # Test for existence since we should probably fail if the file exists
        # but can't be read
        if os.path.exists(osrel_file):
            break
    else:
        return None

    osrel = _parse_source_file(osrel_file)

    if 'ID' in osrel:
        dist = osrel['ID'].lower()
    elif 'NAME' in osrel:
        dist = osrel['NAME'].lower()
    else:
        dist = None

    if dist is None:
        return None

    if 'VERSION_ID' in osrel:
        vers = osrel['VERSION_ID'].lower()
    elif 'VERSION' in osrel:
        vers = osrel['VERSION'].lower()
    else:
        vers = None

    return (dist, vers)


def _read_lsb_release():
    cmd = ['lsb_release', '-a']
    out = None
    lsbrel = None
    try:
        r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = r.communicate()
    except OSError:
        # Executing lsb_release failed, check for /etc/lsb-release anyway
        try:
            lsbrel = _parse_source_file('/etc/lsb-release')
        except:
            pass

    lsb = {}
    if out is not None:
        # Executing lsb_release succeeded, use this data
        for line in out.splitlines():
            splitline = line.split(':', 1)
            if len(splitline) != 2:
                continue
            val = splitline[1].strip().lower()
            if splitline[0] == 'Distributor ID':
                lsb['distributor'] = val
            elif splitline[0] == 'Release':
                lsb['version'] = val
            elif splitline[0] == 'Description':
                lsb['description'] = val
            elif splitline[0] == 'Codename':
                lsb['codename'] = val
    elif lsbrel is not None:
        # /etc/lsb-release format, if the file even exists, is non-standard.
        # Only the `lsb_release` command is specified by LSB. Nonetheless, some
        # distributions install an /etc/lsb-release as part of the base
        # distribution, but `lsb_release` remains optional.
        if 'DISTRIB_ID' in lsbrel:
            # ubuntu, arch, ... ???
            lsb['distributor'] = lsbrel['DISTRIB_ID'].lower()
        if 'DISTRIB_RELEASE' in lsbrel:
            lsb['version'] = lsbrel['DISTRIB_RELEASE'].lower()

    dist = None
    distributor = lsb.get('distributor', None)
    vers = lsb.get('version', None)
    if distributor is not None:
        if distributor.startswith('redhatenterprise'):
            dist = 'rhel'
        elif distributor == 'archlinux':
            dist = 'arch'
        elif distributor.startswith('suse') and lsb.get('description', '').startswith('opensuse'):
            dist = 'opensuse'
        elif distributor.startswith('suse') and lsb.get('description', '').startswith('suse linux enterprise'):
            dist = 'sles'
        elif distributor == 'debian' and vers == 'testing':
            dist = 'debian'
            vers = lsb.get('codename', None)
            if vers is not None and not vers.endswith('/sid'):
                # This is done to ensure the same tag is generated as with
                # /etc/os-release and the legacy method.
                vers = vers + '/sid'
        else:
            # ubuntu, debian, gentoo, scientific, slackware, ... ?
            dist = distributor.split(None, 1)[0].lower()

    if dist is None:
        return None

    return (dist, vers)


_versionish_string = re.compile('\d+(?:\.\d+)*$')

def _extract_version(release):
    """Attempt to determine the version of a distro based on a string that is
    suspected to contain a version-like element toward the end.
    """
    for s in reversed(release.split()):
        if _versionish_string.match(s):
            return s
    return None


def _extract_distribution(release):
    """Attempt to determine the name of a distro based on a string specified by
    the vendor.
    """
    release = release.lower()
    if release.startswith('red hat enterprise'):
        return 'rhel'
    if release.startswith('suse linux enterprise'):
        return 'sles'
    else:
        # ubuntu, gentoo, scientific, opensuse, slackware, ... ?
        return release.split(None, 1)[0].lower()


def _get_platform_legacy():
    # If any distros need specific handling over the globbing at the end, add
    # them to checks. Derivative distributions should be typically be checked
    # before their upstreams.
    # (file, distro map function, version map function)
    checks = (('/etc/arch-release', lambda x: 'arch', lambda x: 'rolling'), # it's an empty file
              ('/etc/slackware-version', _extract_distribution, _extract_version), # -version
              (None, _extract_distribution, _extract_version), # default, will check /etc/*-release
              ('/etc/debian_version', lambda x: 'debian', lambda x: x)) # only contains the release version *or* codename
    for check, dist_f, vers_f in checks:
        if check is None:
            files = glob.glob('/etc/*-release')
            files = filter(lambda x: x not in ('/etc/os-release',
                                               '/etc/lsb-release'), files)
        else:
            files = [check]
        for relfile in files:
            try:
                contents = open(relfile).readline().strip()
                dist = dist_f(contents)
                vers = vers_f(contents)
                if dist is not None:
                    return (dist, vers)
            except (OSError, IOError):
                pass
    return None


def get_specific_platform():
    """Attempt to determine the current platform (Linux distribution + version)
    by (in this order):

    1. Parsing /etc/os-release, if it exists
    2. Parsing the output of `lsb_release -a`, if it exists
    3. Parsing the file /etc/lsb-release, if it exists
    4. Attempting to read distro-specific /etc/*-release files

    If the platform can be determine, a 4-member tuple will be returned:
    (distribution, major version, full version, abi stability). If not, None is
    returned.
    """
    ran_legacy = False
    plat = _read_os_release()
    if plat is None:
        plat = _read_lsb_release()
    if plat is None:
        plat = _get_platform_legacy()
        ran_legacy = True
    if plat is not None:
        dist, vers = plat
        # TODO: should probably try to get the version from lsb_release before
        # legacy
        if vers is None and not ran_legacy:
            legacy = _get_platform_legacy()
            if legacy is not None:
                vers = legacy[1]
        major = _get_major_version(dist, vers)
        stability = _get_stability(dist, vers)
        plat = spectuple(dist, major, vers, stability)
    return plat
