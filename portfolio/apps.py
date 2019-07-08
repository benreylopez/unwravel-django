from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    name = 'portfolio'

    def ready(self):
        from portfolio import updater
        updater.start()


