# -*- coding: utf-8 -*-

from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Manager(object):

    # Tracks each time a Manager instance is created. Used to retain order.
    creation_counter = 0

    # Set to True for the 'objects' managers that are automatically created.
    auto_created = False

    def __new__(cls, *args, **kwargs):
        obj = super(Manager, cls).__new__(cls)
        obj._constructor_args = (args, kwargs)
        return obj

    def __init__(self):
        super(Manager, self).__init__()

        # Increase the creation counter
        self.creation_counter = Manager.creation_counter
        Manager.creation_counter += 1

        self.node = None
        self.name = None
        self._db_alias = None

    def __str__(self):
        return '%s.%s' % (self.node._meta.label, self.name)

    @classmethod
    def _get_backend_methods(cls, backend_class):
        pass

    @classmethod
    def from_backend(cls, backend_class, class_name=None):
        pass

    def contribute_to_class(self, node, name):
        if not self.name:
            self.name = name
        self.node = node

        setattr(node, name, ManagerDescriptor(self))
        self.node._meta.add_manager(self)


class ManagerDescriptor(object):

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError('Manager isn\'t accessible via %s instances' % cls.__name__)

        if cls._meta.abstract:
            raise AttributeError('Manager isn\'t available; %s is abstract' % (
                cls._meta.object_name,
            ))

        return cls._meta.managers_map[self.manager.name]
