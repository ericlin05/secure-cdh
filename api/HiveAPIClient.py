"""
Enabling the Sentry Service for Hive
1. Go to the Hive service.
2. Click the Configuration tab.
3. Select Scope > Hive (Service-Wide).
4. Select Category > Main.
5. Locate the Sentry Service property and select Sentry.
6. Click Save Changes to commit the changes.
Restart the Hive service.

Disable impersonation for HiveServer2 in the Cloudera Manager Admin Console:
1. Go to the Hive service.
2. Click the Configuration tab.
3. Select Scope > HiveServer2.
4. Select Category > Main.
5. Uncheck the HiveServer2 Enable Impersonation checkbox.
6. Click Save Changes to commit the changes.
"""
class HiveAPIClient:
    def __init__(self, hive_service):
        self.service = hive_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
        self.service.update_config({'sentry_enabled': False})

        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('HIVESERVER2') > 0:
                role_group.update_config({
                        'hiveserver2_enable_impersonation': True
                    })
                break

