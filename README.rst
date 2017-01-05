lionshead
=========

A platform detection library for Python. It uses various methods to attempt to
determine the operating system, distribution, release, version, etc., to aid
callers in making platform-specific decisions.

lionshead was originally written for "platform-specific wheels" that were a
solution to the Linux wheel problem before the creation of `manylinux
<https://github.com/pypa/manylinux/>`_. Rather than be wasted effort, it's been
spun in to a separate library (which would've been necessary anyway to be
consumed by both pip and wheel).

Documentation is available at `<http://lionshead.readthedocs.io>`_

Quick start
-----------

On Debian stretch/sid:

>>> from lionshead import *
>>> get_specific_platform()
SpecificPlatform(dist='debian', major_vers='stretch/sid', full_vers='stretch/sid', stability='unstable')
>>> get_specific_platform_string()
'debian-stretch_sid'
>>> get_platform_stability_string()
'unstable'

On CentOS 7:

>>> from lionshead import *
>>> get_specific_platform()
SpecificPlatform(dist='centos', major_vers='7', full_vers='7', stability='stable')
>>> get_specific_platform_string()
'centos-7'
>>> get_platform_stability_string()
'stable'

Installation of the module also installs ``lionshead-platform`` and
``lionshead-stability`` commands that return the output of
:func:`get_specific_platform_string` and :func:`get_platform_stability_string`,
respectively.

FAQ
---

How can I help?
```````````````

See if your OS/distribution is listed and/or correct in `this gist
<https://gist.github.com/natefoo/814c5bf936922dad97ff>`_, and if not, follow
the instructions and create an issue with your findings.

Does this work on anything other than Linux?
````````````````````````````````````````````

Not currently, but as an avid illumos fan, I plan to add support for other
operating systems such as illumos and the BSDs. `Here's the data collection
<https://gist.github.com/natefoo/7af6f3d47bb008669467>`_ I did for Ansible's
illumos detection to get started.

What is a "stable" vs. "unstable" platform?
```````````````````````````````````````````

"Stable" platforms are operating system releases which commit to a defined,
non-changing ABI for the lifetime of the release. This means that the ABI
remains consisntent even after OS updates (this typically means that all
software is maintained at a specific version). Examples of "stable" releases
include:

* Red Hat Enterprise Linux and derivatives
* Ubuntu
* Debian (stable and past stable releases)
* SUSE Linux Enterprise Server
* openSUSE (releases)

Conversely, "unstable" platforms are operating systems that use a "rolling
release" model where software versions can change with each OS update. Examples
of "unstable" releases include:

* Debian (testing/sid)
* openSUSE (tumbleweed)
* Arch

What's with the name?
`````````````````````
The name is a reference to *Indiana Jones and the Last Crusade*, specifically
the scene where Indy takes the "leap of faith" on to the invisible bridge in
the Temple of the Sun.

    "Only in the leap from the lion's head will he prove his worth."

The leap detects the (presence of the) platform underneath... get it? ;P

Code of Conduct
---------------

Everyone interacting in the lionshead project's codebases, issue trackers, chat
rooms, and mailing lists is expected to follow the `PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
