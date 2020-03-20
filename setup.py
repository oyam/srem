#!/usr/bin/env python

import setuptools


readme = open('README.md').read()
long_description = '\n'.join([str(line) for line in readme.split('\n')[9:]])

setuptools.setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
