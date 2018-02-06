#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Scott Coughlin (2018)
#
# This file is part of the gravityspytools django webapp.

"""Setup the gravityspytools package
"""

from __future__ import print_function

import sys
if sys.version < '2.6':
    raise ImportError("Python versions older than 2.6 are not supported.")

import glob
import os.path

from setuptools import (setup, find_packages)

# set basic metadata
PACKAGENAME = 'gravityspytools'
DISTNAME = 'gravityspytools'
AUTHOR = 'Scott Coughlin'
AUTHOR_EMAIL = 'scottcouhlin2014@u.northwestern.edu'
LICENSE = 'BSD 3 LICENSE'

cmdclass = {}

# -- versioning ---------------------------------------------------------------

import versioneer
__version__ = versioneer.get_version()
cmdclass.update(versioneer.get_cmdclass())

# -- dependencies -------------------------------------------------------------

setup_requires = [
    'setuptools',
    'pytest-runner',
]
install_requires = [
    'https://github.com/zooniverse/panoptes-python-client',
    'django',
    'gwpy',
    'psycopg2',
    'sqlalchemy',
    'pandas',
]

# -- run setup ----------------------------------------------------------------

packagenames = find_packages()

setup(name=DISTNAME,
      provides=[PACKAGENAME],
      version=__version__,
      description='A Django webapp providing extra gravityspy tools.',
      url='https://gravityspytools.ciera.northwestern.edu/',
      long_description=None,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=packagenames,
      include_package_data=True,
      cmdclass=cmdclass,
      setup_requires=setup_requires,
      install_requires=install_requires,
      use_2to3=True,
      classifiers=[
          'Programming Language :: Python',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: BSD License v3 (BSDv3)',
      ],
)
