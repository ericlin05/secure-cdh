
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
        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('IMPALAD') > 0:
                role_group.update_config({
                    'impalad_load_balancer': "%s:%s" % (host, self.DEFAULT_HAPROXY_PORT)
                })
                break

    def disable_load_balancer(self):
        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('IMPALAD') > 0:
                role_group.update_config({
                    'impalad_load_balancer': ""
                })
                break
