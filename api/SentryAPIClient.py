
class SentryAPIClient:
    def __init__(self, sentry_service):
        self.service = sentry_service

    def enable_sentry(self):
        """
        Add the Hive, Impala and Hue Groups to Sentry's Admin Groups
        1. Go to the Sentry service.
        2. Click the Configuration tab.
        3. Select Scope > Sentry (Service-Wide).
        4. Select Category > Main.
        5. Locate the Admin Groups property and add the hive, impala and hue groups to the list.
        If an end user is in one of these admin groups, that user has administrative privileges on the Sentry Server.
        6. Click Save Changes to commit the changes.
        """
        for n, config in self.service.get_config(view='full')[0].items():
            if n == "sentry_service_admin_group":
                if config.value is None:
                    self.service.update_config({'sentry_service_admin_group': 'hive,impala,hue'})
                else:
                    values = str(config.value).split(',')
                    if 'hive' not in values:
                        values.append('hive')

                    if 'impala' not in values:
                        values.append('impala')

                    if 'hue' not in values:
                        values.append('hue')

                    self.service.update_config({'sentry_service_admin_group': ",".join(values)})

                break
