# -*- coding: utf-8 -*-

import inspect

from django.utils import six
from py2neo.ogm import GraphObjectType, GraphObjectSelector

from tracer.nodes.options import Options
from tracer.nodes.manager import Manager


class Meta(GraphObjectType):
    """
    Metaclass for ``GraphObject``.
    """

    def __new__(mcs, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, Meta)]
        if not parents:
            return super(Meta, mcs).__new__(mcs, str(name), bases, attrs)

        module = attrs.pop('__module__')
        new_class = super(Meta, mcs).__new__(mcs, str(name), bases, {'__module__': module})

        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        meta = attr_meta or getattr(new_class, 'Meta', None)

        new_class.add_to_class('_meta', Options(meta, app_label=None))
        if not abstract:
            # TODO: Handle this
            pass

        # Add all attributes to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        if abstract:
            attr_meta.abstract = False
            new_class.Meta = attr_meta
            return new_class

        new_class._prepare()
        # TODO: Register model if we'd like to have a register

        return new_class

    @property
    def _base_manager(cls):
        return cls._meta.base_manager

    @property
    def _default_manager(cls):
        return cls._meta.default_manager

    def _prepare(cls):
        """
        Prepares the the class
        """
        opts = cls._meta
        opts._prepare(cls)

        if not opts.managers:
            if any(f.name == 'objects' for f in opts.fields):
                raise ValueError('GraphObject %s must specify a custom Manager, because'
                                 'it has a field named \'objects\'.' % cls.__name__)
            manager = Manager()
            manager.auto_created = True
            cls.add_to_class('objects', manager)

    def add_to_class(cls, name, value):
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class GraphObjectMixin(six.with_metaclass(Meta)):
    """
    A Mixin class for ``GraphObject``.
    Let GraphObjects perform operations on the database itself.
    """

    def _get_connection(self, using=None):
        from tracer import connections
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
        from tracer import connections
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

