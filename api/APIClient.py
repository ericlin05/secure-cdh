from cm_api.api_client import ApiResource
from ImpalaAPIClient import ImpalaAPIClient
from HiveAPIClient import HiveAPIClient
from HbaseAPIClient import HbaseAPIClient

import importlib

class APIClient:
    def __init__(self, cm_host, cm_user, cm_pass,
                 cluster_name=None):
        self.SERVICE_HIVE   = 'HIVE'
        self.SERVICE_HUE    = 'HUE'
        self.SERVICE_IMPALA = 'IMPALA'
        self.SERVICE_SOLR   = 'SOLR'
        self.SERVICE_YARN   = 'YARN'
        self.SERVICE_HDFS   = 'HDFS'
        self.SERVICE_HBASE  = 'HBASE'
        self.SERVICE_ZK     = 'ZOOKEEPER'
        self.SERVICE_SENTRY = 'SENTRY'

        self.api = ApiResource(
            cm_host,
            username=cm_user,
            password=cm_pass,
        )

        self.cluster = None
        self.services = {}
        for c in self.api.get_all_clusters():
            if cluster_name is None or cluster_name == c.name:
                self.cluster = c
                break

        for service in self.cluster.get_all_services():
            self.services[service.type] = service

    def has_sentry(self):
        """
        This function checks if sentry service is available in the cluster
        :return: boolean
        """
        return self.SERVICE_SENTRY in self.services

    def has_hbase(self):
        """
        This function checks if hbase service is available in the cluster
        :return: boolean
        """
        return self.SERVICE_HBASE in self.services

    def get_impala_service(self):
        """
        This function checks if sentry service is available in the cluster
        :return: boolean
        """
        if self.SERVICE_IMPALA in self.services:
            return self.services[self.SERVICE_IMPALA]

        return None

    def get_hiveserver2_service(self):
        """
        This function returns the hiveserver2 service instance
        :return: boolean
        """
        if self.SERVICE_HIVE in self.services:
            return self.services[self.SERVICE_HIVE]

        return None

    def get_hbase_service(self):
        """
        This function returns the hbase service instance
        :return: boolean
        """
        if self.SERVICE_HBASE in self.services:
            return self.services[self.SERVICE_HBASE]

        return None

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

    def enable_kerberos(self):
        service_list = [
            self.SERVICE_HDFS,
            self.SERVICE_ZK,
            self.SERVICE_HBASE,
            self.SERVICE_SOLR
        ]

        for s_name in service_list:
            if s_name in self.services:
                className = s_name.capitalize() + "APIClient"
                module = importlib.import_module("api."+className)
                class_ = getattr(module, className)
                client = class_(self.services[s_name])
                client.enable_kerberos()

    def enable_impala_vip(self, host):
        impala_service = self.get_impala_service()
        ImpalaAPIClient(impala_service).enable_load_balancer(host)

    def disable_impala_vip(self):
        impala_service = self.get_impala_service()
        ImpalaAPIClient(impala_service).disable_load_balancer()

    def hiveserver2_create_role(self, host, i):
        hive_service = self.get_hiveserver2_service()
        HiveAPIClient(hive_service).add_hs2_role(host, i)

    def enable_hive_vip(self, host):
        service = self.get_hiveserver2_service()
        HiveAPIClient(service).enable_load_balancer(host)

    def disable_hive_vip(self):
        service = self.get_hiveserver2_service()
        HiveAPIClient(service).disable_load_balancer()

    def enable_hbase_authorization(self):
        service = self.get_hbase_service()
        HbaseAPIClient(service).enable_authorization()