# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.utils import six
from django.core.exceptions import ImproperlyConfigured

from py2neo.ogm import GraphObjectType, GraphObjectSelector

from .constants import DEFAULT_ALIAS


class Meta(type):
    """
    Template for the ``GraphObjectMixin.Meta`` class.
    """

    db_alias = DEFAULT_ALIAS
    abstract = False

    def __new__(mcs, name, bases, attrs):
        attrs.setdefault('abstract', mcs.abstract)
        attrs.setdefault('db_alias', mcs.db_alias)
        cls = super(Meta, mcs).__new__(mcs, str(name), bases, attrs)
        return cls

    def __setattr__(cls, key, value):
        raise AttributeError('Meta class is immutable')

    def __delattr__(self, item):
        raise AttributeError('Meta class is immutable')


class GraphObjectMeta(GraphObjectType):
    """
    Make sure all classes that implements the Meta type
    gets a Meta class.
    """

    def __new__(mcs, name, bases, attrs):
        cls = super(GraphObjectMeta, mcs).__new__(mcs, str(name), bases, attrs)

        if hasattr(cls, 'Meta'):
            cls.Meta = Meta('Meta', (Meta,), dict(cls.Meta.__dict__))
        elif not cls.__abstract__:
            raise ImproperlyConfigured('%s must implement a Meta class or '
                                       'set the `__abstract__` attribute to True.' % name)

        return cls


class GraphObjectMixin(six.with_metaclass(GraphObjectMeta)):
    """
    A Mixin class for ``GraphObject``.
    Let GraphObjects perform operations on the database itself.
    """

    __abstract__ = True

    @property
    def db_alias(self):
        return self.Meta.db_alias

    def _get_connection(self, using=None):
        from . import connections
        using = using or self.db_alias
        return connections[using].get_backend()
    
    @classmethod
    def select(cls, primary_value=None, using=None):
        """
        Select one or more nodes from the database, wrapped as instances of this class.

        :param primary_value: value of the primary property (optional)
        :param using: The database alias to use for connection to the server.
        :rtype: :class:`.GraphObjectSelection`
        """
        from . import connections
        using = using or cls.Meta.db_alias
        return GraphObjectSelector(cls, connections[using].get_backend()).select(primary_value)
    
    def create(self, using=None):
        """
        Create a new node on the server.
        """
        return self._get_connection(using).create(self)

    def delete(self, using=None):
        """
        Delete the remote node and relationships that correspond to
        the given GraphObject.
        """
        return self._get_connection(using).delete(self)

    def push(self, using=None):
        """
        Update the node with changes from the ``GraphObject`` and its
        associated ``RelatedObject`` instances. If a remote node does not
        exist, one will be created. If one exist, it will be updated. The
        set of outgoing relationships will be adjusted to match those
        described by the ``RelatedObject`` instances.
        """
        return self._get_connection(using).push(self)

    def pull(self, using=None):
        """
        Update a ``GraphObject`` and its associated ``RelatedObject``
        instances with changes from the graph.
        """
        return self._get_connection(using).pull(self)

    def merge(self, using=None):
        """
        For a ``GraphObject``, create and merge are an identical operation.
        This is because ``GraphObject`` instances have uniqueness defined
        by their primary label and primary key thus both operations can
        be considered a for of merge.

        If a corresponding remote node does not exist, one will be created.
        Unlike push, however, no update will occur if a node already exists.
        """
        return self._get_connection(using).merge(self)

