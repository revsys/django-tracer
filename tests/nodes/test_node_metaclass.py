# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from tracer.nodes import GraphObjectMixin


class NodeMetaTestCase(TestCase):

    def setUp(self):

        class PersonNode(GraphObjectMixin, GraphObject):

            # class Meta:
            #     abstract = True

            __primarykey__ = 'name'

            name = Property()

        self.PersonNode = PersonNode

    def test_init_node_without_metaclass(self):
        person = self.PersonNode()
        self.assertIsInstance(person, self.PersonNode)

