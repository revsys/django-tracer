# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.utils.functional import cached_property
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.text import camel_case_to_spaces
from django.utils.translation import string_concat

from tracer.constants import DEFAULT_ALIAS

DEFAULT_NAMES = (
    'abstract', 'apps', 'app_label', 'base_manager_name',
    'db_alias', 'default_manager_name', 'ordering',
    'verbose_name', 'verbose_name_plural'
)


@python_2_unicode_compatible
class Options(object):

    default_apps = apps

    def __init__(self, meta, app_label=None):
        self.abstract = False
        self.apps = self.default_apps
        self.app_label = app_label
        self.base_manager_name = None
        self.db_alias = DEFAULT_ALIAS
        self.default_manager_name = None
        self.local_managers = []
        self.meta = meta
        self.node_name = None
        self.object_name = None
        self.ordering = []
        self.verbose_name = None
        self.verbose_name_plural = None

        # Store the original user-defined values for each option,
        # for use when serializing the node definition.
        self.original_attrs = {}

    def __repr__(self):
        return '<Options for %s>' % self.object_name

    def __str__(self):
        return "%s.%s" % (smart_text(self.app_label), smart_text(self.node_name))

    @property
    def label(self):
        return '%s.%s' % (self.app_label, self.object_name)

    @property
    def label_lower(self):
        return '%s.%s' % (self.app_label, self.node_name)

    @property
    def app_config(self):
        return self.apps.app_configs.get(self.app_label)

    @cached_property
    def base_manager(self):
        pass

    @cached_property
    def default_manager(self):
        pass

    @cached_property
    def managers(self):
        # TODO: Implement
        return []

    @cached_property
    def managers_map(self):
        return {manager.name: manager for manager in reversed(self.managers)}

    def _prepare(self, node):
        # TODO: Set up ordering
        # TODO: Set up some kind of "pk" attribute
        pass

    def add_manager(self, manager):
        self.local_managers.append(manager)
        self._expire_cache()

    def contribute_to_class(self, cls, name):

        cls._meta = self
        self.node = cls
        self.object_name = cls.__name__
        self.node_name = self.object_name.lower()
        self.verbose_name = camel_case_to_spaces(self.object_name)

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('__'):
                    del meta_attrs[name]

            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

            # verbose_name_plural is a special case because it uses a 's'
            # by default.
            if self.verbose_name_plural is None:
                self.verbose_name_plural = string_concat(self.verbose_name, 's')

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s" % ','.join(meta_attrs.keys()))

        else:
            self.verbose_name_plural = string_concat(self.verbose_name, 's')
        del self.meta


