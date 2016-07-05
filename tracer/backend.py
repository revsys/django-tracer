# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from py2neo.database import Graph

from .constants import DEFAULT_ALIAS


class Neo4jBackend(object):
    """
    The Neo4j backend connection
    """

    def __init__(self, using, **options):
        if 'URL' not in options:
            raise ImproperlyConfigured('You must specify a "URL" in your settings for connection "%s".' % using)

        self.using = using
        self.conn = Graph(options['URL'])
        self.logger = logging.getLogger('neo4j')

    ####################
    # PROXIES TO GRAPH #
    ####################

    @property
    def dbms(self):
        """
        Returns the database management system to which this backend
        connection instance belongs.

        @:returns: A ``py2neo.database.DBMS`` instance.
        """
        return self.conn.dbms

    @property
    def node_labels(self):
        """
        The set of node labels currently defined within the graph.
        """
        return self.conn.node_labels

    @property
    def relationship_types(self):
        """
        The set of relationship types currently defined within the graph.
        """
        return self.conn.relationship_types

    @property
    def schema(self):
        """
        The schema resource for this graph.
        """
        return self.conn.schema

    def create(self, subgraph):
        """
        Run a ``Transaction.create()`` operation within an autocommit transaction.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: None.
        """
        return self.conn.create(subgraph)

    def degree(self, subgraph):
        """
        Run a ``Transaction.degree()`` operation within an autocommit transaction.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: The total degree of all nodes in the subgraph.
        """
        return self.conn.degree(subgraph)

    def delete(self, subgraph):
        """
        Run a ``Transaction.delete()`` operation withing an autocommit transaction.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: None.
        """
        return self.conn.delete(subgraph)

    def delete_all(self):
        """
        Delete *all* nodes and relationships from this graph.
        Warning: This operation *cannot* be undone!
        """
        return self.conn.delete_all()

    def evaluate(self, statement, parameters=None, **kwargs):
        """
        Run a ``Transaction.evaluate()`` operation within an autocommit transaction.

        @:param statement: Cypher statement.
        @:param parameters: A dict of parameters.
        @:param kwargs: Keyword parameters.
        @:returns: The first value from the first record or None.
        """
        return self.conn.evaluate(statement, parameters, **kwargs)

    def exists(self, subgraph):
        """
        Run a ``Transaction.exists()`` operation within an autocommit transaction.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: Unknown (TODO: Update).
        """
        return self.conn.exists(subgraph)

    def find(self, *args, **kwargs):
        """
        Yield all nodes with a given label, optionally filtering by property
        key and value.

        @:param label: Node or Label to match.
        @:param property_key: Property key to match.
        @:param property_value: Property value to match. If a tuple or set is provider,
                                any of these values may be matched.
        @:param limit: Maximum number of nodes to match.
        @:returns: Unknown (TODO: Update).
        """
        yield self.conn.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        """
        Find a single node by label and optional property. This method is inteded to be used
        with a unique constrain and does not fail if more than one matching node is found.

        @:param label: Node or Label to match.
        @:param property_key: Property key to match.
        @:param property_value: Property value to match. If a tuple or set is provider,
                                any of these values may be matched.
        @:returns: Unknown (TODO: Update).
        """
        return self.conn.find_one(*args, **kwargs)

    def match(self, start_node=None, rel_type=None, end_node=None, bidirectional=False, limit=None):
        """
        Match and return all relationships with specific criteria.
        
        @:param start_node: Start node of relationships to match. None means any node.
        @:param rel_type: Type of relationships to match. None means any type.
        @:param end_node: End node of relationships to match. None means any node.
        @:param bidirectional: True if reversed relationships should also be included.
        @:param limit: Maximum number of relationships to match. None means unlimited.
        @:returns: All relationships which match criteria.
        """
        return self.conn.match(start_node, rel_type, end_node, bidirectional, limit)

    def match_one(self, start_node=None, rel_type=None, end_node=None, bidirectional=False):
        """
        Match and return all relationships with specific criteria.

        @:param start_node: Start node of relationships to match. None means any node.
        @:param rel_type: Type of relationships to match. None means any type.
        @:param end_node: End node of relationships to match. None means any node.
        @:param bidirectional: True if reversed relationships should also be included.
        @:returns: One relationship which match specific criteria.
        """
        return self.conn.match_one(start_node, rel_type, end_node, bidirectional)
        
    def merge(self, subgraph, label=None, *property_keys):
        """
        Run a ``Transaction.merge()`` operation within an autocommit transaction.
        
        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:param label: Label on which to match any existing nodes.
        @:param property_keys: Property keys on which to match any existing nodes.
        @:returns: Unknown (Update).
        """
        return self.conn.merge(subgraph, label, *property_keys)
        
    def node(self, id):
        """
        Fetch a node by ID. This method creates an object representing the remote
        node with the ID specified but fetches no data from the server. For this
        reason, there is no guarantee that the entity returned actually exists.

        @:param id: The ID of a node.
        @:returns: GraphObject
        """
        return self.conn.node(id)

    def pull(self, subgraph):
        """
        Pull data to one or more entities from their remote counterparts.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: Unknown (Update).
        """
        return self.conn.pull(subgraph)

    def push(self, subgraph):
        """
        Push data from one or more entities to their remote counterparts.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: Unknown (Update).
        """
        return self.conn.push(subgraph)

    def relationship(self, id):
        """
        Fetch a relationship by ID.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: Unknown (Update).
        """
        return self.conn.relationship(id)

    def run(self, statement, parameters=None, **kwargs):
        """
        Run a ``Transaction.run()`` operation within an autocommit transaction.

        @:param statement: Cypher statement.
        @:param parameters: Dictionary of parameters.
        @:param kwargs: Not documented.
        @:returns: Unknown (Update).
        """
        return self.conn.run(statement, parameters, **kwargs)

    def separate(self, subgraph):
        """
        Run a ``Transaction.separate()`` operation within an autocommit transaction.

        @:param subgraph: A Node, RelationShip or other Subgraph.
        @:returns: Unknown (Update).
        """
        return self.conn.separate(subgraph)


class Neo4jEngine(object):
    """
    The Neo4j backend engine
    """

    backend = Neo4jBackend

    def __init__(self, using=None):
        if using is None:
            using = DEFAULT_ALIAS

        self.using = using
        self.options = settings.NEO4J_CONNECTIONS.get(self.using, {})
        self._backend = None

    # def __repr__(self):
    #     return '<%s: %s>' % (self.__class__.__name__, self.using)

    def get_backend(self):
        if self._backend is None:
            self._backend = self.backend(self.using, **self.options)
        return self._backend

    def reset_sessions(self):
        """
        Reset any transient connections, file handles, etc.
        """
        self._backend = None
