# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from tracer import loading
from tracer.constants import DEFAULT_ALIAS

__title__ = "tracer"
__version__ = "0.0.1"
__author__ = "Rolf Håvard Blindheim"
__license__ = "MIT License"
VERSION = __version__

default_app_config = 'tracer.apps.TracerConfig'


if not hasattr(settings, 'NEO4J_CONNECTIONS'):
    raise ImproperlyConfigured('The NEO4J_CONNECTIONS setting is required.')

if DEFAULT_ALIAS not in settings.NEO4J_CONNECTIONS:
    raise ImproperlyConfigured('The default alias "%s" must be included '
                               'in the NEO4J_CONNECTIONS setting.' % DEFAULT_ALIAS)

# Load connections
connections = loading.ConnectionHandler(settings.NEO4J_CONNECTIONS)
