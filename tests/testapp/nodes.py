# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from tracer.nodes import GraphObjectMixin


class Movie(GraphObjectMixin, GraphObject):
    """
    Represents a ``Movie`` node
    """

    __primarykey__ = 'title'

    title = Property()
    tag_line = Property('tagline')
    released = Property()

    actors = RelatedFrom('Person', 'ACTED_IN')
    directors = RelatedFrom('Person', 'DIRECTED')
    producers = RelatedFrom('Person', 'PRODUCED')


class Person(GraphObjectMixin, GraphObject):
    """
    Represents a ``Person`` node
    """

    __primarykey__ = 'name'

    name = Property()
    born = Property()

    acted_in = RelatedTo(Movie)
    directed = RelatedTo(Movie)
    produced = RelatedTo(Movie)
