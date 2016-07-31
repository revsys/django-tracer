# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from tracer.loading import ConnectionHandler


class ConnectionHandlerTestCase(TestCase):

    def test_class_init(self):
        handler = ConnectionHandler({})
        self.assertEqual(handler.connections_info, {})

        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            }
        })
        self.assertEqual(handler.connections_info, {
            'default': {
                'URL': 'http://localhost:7474'
            }
        })

    def test_get_all_connections(self):
        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            },
            'other': {
                'URL': 'http://otherhost:7474'
            }
        })

        for engine in map(lambda e: repr(e).strip('<>').split(' object at ')[0], handler.all()):
            self.assertEqual(engine, 'tracer.backend.Neo4jEngine')

    def test_get_item(self):
        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            }
        })
        engine = handler['default']

        from tracer.backend import Neo4jEngine
        self.assertIsInstance(engine, Neo4jEngine)

    def test_get_item_same_instance(self):
        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            }
        })

        # Make sure we get the same item when getting by same alias
        path1, address1 = repr(handler['default']).strip('<>').split(' object at ')
        path2, address2 = repr(handler['default']).strip('<>').split(' object at ')
        self.assertEqual(path1, path2)
        self.assertEqual(address1, address2)

    def test_get_item_invalid_alias(self):
        handler = ConnectionHandler({})
        try:
            handler['default']
            self.fail('Did not fail when trying to get a non-existing connection alias.')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The key "default" isn\'t an available connection.')

    def test_reload(self):
        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            }
        })

        # Make sure we get a new object when reloaded
        self.assertNotEqual(handler['default'], handler.reload('default'))

    def test_reload_invalid_alias(self):
        handler = ConnectionHandler({
            'default': {
                'URL': 'http://localhost:7474'
            }
        })

        try:
            handler.reload('slave')
        except ImproperlyConfigured as e:
            self.assertEqual(str(e), 'The key "slave" isn\'t an available connection.')
        else:
            self.fail('Should fail with ImproperlyConfigured when reloading an invalid alias.')
