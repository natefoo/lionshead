#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os.path import join
from setuptools import setup, find_packages


with open('README.rst') as file:
    long_description = file.read()

long_description += '\n\n'
with open('HISTORY.rst') as file:
    long_description += file.read()

# Strip RTD :doc: links for PyPI
long_description = long_description.replace(':doc:', '')

init = join('lionshead', '__init__.py')
with open(init) as f:
    exec(compile(f.read(), "somefile.py", 'exec'))


setup(
    name = 'lionshead',
    version = __version__,
    packages = find_packages(),
    description = 'Detect OS/platforms',
    long_description = long_description,
    url = 'https://github.com/natefoo/lionshead',
    author = 'Nate Coraor',
    author_email = 'nate@coraor.org',
    license = 'MIT',
    keywords = 'platform os operating system',
    entry_points = {
        'console_scripts': [
            'lionshead-platform = lionshead:get_specific_platform_string',
            'lionshead-stability = lionshead:get_platform_stability_string',
        ]
    },
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
)
