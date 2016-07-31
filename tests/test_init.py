# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.utils.six.moves import reload_module

import tracer


class MissingConnectionsDeclarationTestCase(TestCase):

    @override_settings()
    def test_import(self):
        del settings.NEO4J_CONNECTIONS
        try:
            reload_module(tracer)
            self.fail('Did not fail when missing "NEO4J_CONNECTIONS" in settings.')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The NEO4J_CONNECTIONS setting is required.')


@override_settings(NEO4J_CONNECTIONS={})
class MissingDefaultAliasTestCase(TestCase):

    def test_import(self):
        try:
            reload_module(tracer)
            self.fail('Did not fail when importing tracer without defining the '
                      '"DEFAULT_ALIAS" in NEO4J_CONNECTIONS.')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The default alias "default" must be included '
                                     'in the NEO4J_CONNECTIONS setting.')


