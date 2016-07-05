#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals


import os
import sys
import nose


def start(argv=None):
    sys.exitfunc = lambda: sys.stderr.write('Shutting down...\n')

    if argv is None:
        argv = [
            'nosetests',
            '--with-coverage',
            '--cover-html',
            '--cover-html-dir=.htmlcov',
            '--cover-erase',
            '--cover-branches',
            '--cover-inclusive',
            '--cover-package=tracer'
        ]

    nose.run_exit(argv=argv, defaultTest=os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    start(sys.argv)
