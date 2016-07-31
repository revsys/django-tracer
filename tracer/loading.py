# -*- coding: utf-8 -*-

import threading

from django.core.exceptions import ImproperlyConfigured

from .backend import Neo4jEngine


class ConnectionHandler(object):
    """
    Manage connection for the local thread.
    """

    def __init__(self, connections_info):
        self.connections_info = connections_info
        self.thread_local = threading.local()

    def __getitem__(self, item):
        if not hasattr(self.thread_local, 'connections'):
            self.thread_local.connections = {}
        elif item in self.thread_local.connections:
            return self.thread_local.connections[item]

        self.ensure_defaults(item)
        self.thread_local.connections[item] = Neo4jEngine(using=item)
        return self.thread_local.connections[item]

    def all(self):
        return [self[alias] for alias in self.connections_info]

    def ensure_defaults(self, alias):
        try:
            self.connections_info[alias]
        except KeyError:
            raise ImproperlyConfigured('The key "%s" isn\'t an available connection.' % alias)

    def reload(self, alias):
        if not hasattr(self.thread_local, 'connections'):
            self.thread_local.connections = {}
        try:
            del self.thread_local.connections[alias]
        except KeyError:
            pass

        return self.__getitem__(alias)
