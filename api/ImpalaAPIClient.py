
class ImpalaAPIClient:

    def __init__(self, impala_service):
        self.service = impala_service
        self.DEFAULT_HAPROXY_PORT = 25003

    def enable_sentry(self):
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
        self.service.update_config({'sentry_service': 'sentry'})
        self.service.update_config({'sentry_enabled': False})

    def enable_load_balancer(self, host):
        self.service.update_config({'impalad_load_balancer': "%s:%s" % (host, self.DEFAULT_HAPROXY_PORT)})

    def disable_load_balancer(self):
        self.service.update_config({'impalad_load_balancer': ""})
