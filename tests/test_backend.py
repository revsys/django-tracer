# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from tracer import connections


class Neo4jBackendTestCase(TestCase):
    """
    Testing the ``tracer.backend.Neo4jBackend`` backend.
    """

    def setUp(self):
        self.backend = connections['default']
