#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

:author: Josh Moore <josh@glencoesoftware.com>

Installation script for Corgi

Copyright (C) 2014 Glencoe Software, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from setuptools import setup


VERSION = "0.2.0"

LONG_DESCRIPTION = open("README.rst", "r").read()

CLASSIFIERS = ["Development Status :: 4 - Beta",
               "Environment :: Console",
               "Intended Audience :: Developers",
               ("License :: OSI Approved ::",
                " GNU General Public License v2 (GPLv2)"),
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Software Development :: Version Control"]

REQUIREMENTS = open("requirements.txt", "r").read()
REQUIREMENTS = [line.strip() for line in REQUIREMENTS.split("\n")
                if line.strip() and not line.strip().startswith("#")]

setup(name='corgi',

      # Simple strings
      author='Glencoe Software',
      author_email='corgi@glencoesoftware.com',
      description='DevTools Integrator',
      license='GPLv2',
      url='https://github.com/glencoesoftware/corgi',

      # More complex variables
      py_modules=["corgi_loves"],
      install_requires=REQUIREMENTS,
      entry_points={'console_scripts': ['corgi=corgi_loves:entry_point']},
      data_files=[('.', ['LICENSE.txt', 'README.rst', 'requirements.txt'])],
      ## zip_safe=False,  # For reading RELEASE-VERSION

      # Using global variables
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      version=VERSION,
      )
