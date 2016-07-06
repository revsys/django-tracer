# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from tracer import constants


class ConstantsTestCase(TestCase):
    """
    Make sure constants are what's expected.
    """

    def test_default_alias(self):
        self.assertEqual(constants.DEFAULT_ALIAS, 'default')
