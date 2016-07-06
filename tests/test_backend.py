# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from tracer.backend import Neo4jBackend, Neo4jEngine
from tracer.constants import DEFAULT_ALIAS


class Neo4jBackendTestCase(TestCase):
    """
    Testing the ``tracer.backend.Neo4jBackend`` class.
    """

    def setUp(self):
        self.config = {
            'default': {
                'URL': 'http://localhost:7474'
            },
            'invalid': {
                'NOT_URL': 'http://example.com:7474'
            }

        }

    def test_init(self):
        options = self.config['default']
        backend = Neo4jBackend(using='default', **options)
        self.assertIsInstance(backend, Neo4jBackend)

    def test_init_invalid(self):
        options = self.config['invalid']
        try:
            Neo4jBackend(using='invalid', **options)
            self.fail("Did not fail when initializing with invalid options.")
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'You must specify a "URL" in your settings for connection "invalid".')


@override_settings(
    NEO4J_CONNECTIONS={
        'default': {},
        'other': {
            'URL': 'http://localhost:7474'
        }})
class Neo4jEngineTestCase(TestCase):
    """
    Testing the ``tracer.backend.Neo4jEngine`` class.
    """

    def test_init_provided_using(self):
        engine = Neo4jEngine(using='other')
        self.assertEqual(engine.using, 'other')

    def test_init_without_using_sets_default_alias(self):
        engine = Neo4jEngine(using=None)
        self.assertEqual(engine.using, DEFAULT_ALIAS)

    def test_get_backend(self):
        engine = Neo4jEngine(using='other')
        self.assertEqual(engine._backend, None)

        backend = engine.get_backend()
        self.assertIsInstance(backend, Neo4jEngine.backend)
        self.assertIsInstance(engine._backend, Neo4jEngine.backend)
        self.assertEqual(backend, engine._backend)

    def test_reset_sessions(self):
        engine = Neo4jEngine(using='other')
        backend = engine.get_backend()
        self.assertEqual(backend, engine._backend)

        engine.reset_sessions()
        self.assertEqual(engine._backend, None)

