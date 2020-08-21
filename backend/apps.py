from django.apps import AppConfig
import os


class BackendConfig(AppConfig):
    name = 'backend'
    scheduler = False

    def ready(self):
        from db_updater import updater
        if os.environ.get('RUN_MAIN', None) != 'true':
            updater.start()
            self.scheduler = True
