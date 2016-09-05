
class ImpalaAPIClient:
    def __init__(self, impala_service):
        self.service = impala_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
        self.service.update_config({'sentry_enabled': False})
