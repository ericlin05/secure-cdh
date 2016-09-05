
class HiveAPIClient:
    def __init__(self, hive_service):
        self.service = hive_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
        self.service.update_config({'sentry_enabled': False})
