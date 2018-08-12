# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class App1Config(AppConfig):
    name = 'app_1'

    def ready(self):
        import signals.handlers
