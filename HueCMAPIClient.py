import json

class HueCMAPIClient():
    def __init__(self, api):
        self.api = api
        self.config_url = api.get_config_url(
            api.get_service_name(api.SERVICE_HUE.upper())
        )

    def enable_sentry(self):
        data = {"items" : [ { "name" : "sentry_service", "value" : "sentry" } ] }
        self.api.curl_put(self.config_url, json.dumps(data))