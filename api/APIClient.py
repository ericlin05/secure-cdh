from cm_api.api_client import ApiResource
from cm_api.api_client import API_CURRENT_VERSION
import importlib

class APIClient:
    def __init__(self, cm_host, cm_user, cm_pass,
                 version=API_CURRENT_VERSION,
                 cluster_name=None):
        self.SERVICE_HIVE   = 'HIVE'
        self.SERVICE_HUE    = 'HUE'
        self.SERVICE_IMPALA = 'IMPALA'
        self.SERVICE_SOLR   = 'SOLR'
        self.SERVICE_YARN   = 'YARN'

        self.api = ApiResource(
            cm_host,
            username=cm_user,
            password=cm_pass,
            version=version
        )

        self.cluster = None
        self.services = {}
        for c in self.api.get_all_clusters():
            if cluster_name is None or cluster_name == c.name:
                self.cluster = c
                break

        for service in self.cluster.get_all_services():
            self.services[service.type] = service

    def enable_sentry(self):
        service_list = [
            self.SERVICE_HIVE,
            self.SERVICE_IMPALA,
            self.SERVICE_YARN,
            self.SERVICE_HUE
        ]

        for s_name in service_list:
            if s_name in self.services:
                className = s_name.capitalize() + "APIClient"
                module = importlib.import_module("api."+className)
                class_ = getattr(module, className)
                client = class_(self.services[s_name])
                client.enable_sentry()

