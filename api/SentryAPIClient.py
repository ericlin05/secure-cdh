
class SentryAPIClient:
    def __init__(self, sentry_service):
        self.service = sentry_service

    def enable_sentry(self):
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
