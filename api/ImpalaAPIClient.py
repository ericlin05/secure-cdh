"""
Enabling the Sentry Service for Impala
1. Enable the Sentry service for Hive (as instructed above).
2. Go to the Impala service.
3. Click the Configuration tab.
4. Select Scope > Impala (Service-Wide).
5. Select Category > Main.
6. Locate the Sentry Service property and select Sentry.
7. Click Save Changes to commit the changes.
8. Restart Impala.
"""
class ImpalaAPIClient:
    def __init__(self, impala_service):
        self.service = impala_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
        self.service.update_config({'sentry_enabled': False})
