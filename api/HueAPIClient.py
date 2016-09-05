
class HueAPIClient:
    def __init__(self, hue_service):
        self.service = hue_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
