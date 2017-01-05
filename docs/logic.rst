Platform detection logic
========================

Linux
-----

On Linux, platform detection follows the sequence:

1. Parse ``/etc/os-release``, if it exists
2. Parse the output of the ``lsb_release -a`` command, if it exists
3. Parse the file ``/etc/lsb-release``, if it exists
4. Attempt to read distro-specific ``/etc/*-release`` files

``/etc/os-release`` is a standardized file format defined by the systemd
project. All distributions that support systemd provide it, and even some
distributions that do not support systemd still ship the file. This is the
preferred method.

The Linux Standard Base (LSB) system is used as a fallback. This system is
optional on most distributions, and can be installed in components. For
example, sometimes ``/etc/lsb-release`` is installed but the ``lsb_release``
command, which is the only official LSB-defined method for reading LSB release
values, is not.

If none of the above can be found, other known OS-specific methods will be
used, e.g. the presence of ``/etc/debian_version``, ``/etc/arch-release``, or
``/etc/slackware-version``.
