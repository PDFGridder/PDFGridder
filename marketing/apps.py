from django import apps


class MarketingConfig(apps.AppConfig):
    name = 'marketing'

    def ready(self):
        from .listeners import *
