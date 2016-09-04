import pycurl
import json
from StringIO import StringIO

class CMAPI:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.api_url = "{0}/api/{1}".format(
            self.host,
            self.get_version()
        )

        self.cluster_name = self.get_cluster_name()

        self.hive_service_name = None
        self.yarn_service_name = None
        self.impala_service_name = None
        self.hue_service_name = None
        self.solr_service_name = None

        self.hive_config_url = None
        self.yarn_config_url = None
        self.impala_config_url = None
        self.hue_config_url = None
        self.solr_config_url = None

        self.get_service_names()

        if self.hive_service_name is not None:
            self.hive_config_url = "{0}/clusters/{1}/services/{2}/config".format(
                self.api_url,
                self.cluster_name,
                self.hive_service_name
            )

        if self.yarn_service_name is not None:
            self.yarn_config_url = "{0}/clusters/{1}/services/{2}/config".format(
                self.api_url,
                self.cluster_name,
                self.yarn_service_name
            )

        if self.impala_service_name is not None:
            self.impala_config_url = "{0}/clusters/{1}/services/{2}/config".format(
                self.api_url,
                self.cluster_name,
                self.impala_service_name
            )

        if self.hue_service_name is not None:
            self.hue_config_url = "{0}/clusters/{1}/services/{2}/config".format(
                self.api_url,
                self.cluster_name,
                self.hue_service_name
            )

        if self.solr_service_name is not None:
            self.solr_config_url = "{0}/clusters/{1}/services/{2}/config".format(
                self.api_url,
                self.cluster_name,
                self.solr_service_name
            )

    def curl_get(self, url):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, "%s:%s" % (self.username, self.password))
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        c.close()

        return buffer.getvalue()

    def curl_put(self, url, data):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: application/json'])
        c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, "%s:%s" % (self.username, self.password))
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        c.close()

        return buffer.getvalue()

    def get_services(self):
        url = "{0}/clusters/{1}/services".format(
            self.api_url,
            self.cluster_name
        )
        return self.curl_get(url)

    def get_version(self):
        url = "{0}/api/version".format(self.host)
        return self.curl_get(url)

    def get_cluster_name(self):
        url = "{0}/clusters".format(self.api_url)
        data = json.loads(self.curl_get(url))

        return data["items"][0]["name"]

    def get_service_names(self):
        url = "{0}/clusters/{1}/services".format(self.api_url, self.cluster_name)
        data = json.loads(self.curl_get(url))
        for d in data["items"]:
            if d["type"] == "HIVE":
                self.hive_service_name = d["name"]

            if d["type"] == "YARN":
                self.yarn_service_name = d["name"]

            if d["type"] == "IMPALA":
                self.impala_service_name = d["name"]

            if d["type"] == "HUE":
                self.hue_service_name = d["name"]

            if d["type"] == "SOLR":
                self.solr_service_name = d["name"]

    def get_hive_configs(self):
        return self.curl_get(self.hive_config_url + "?view=full")

    def get_yarn_configs(self):
        return self.curl_get(self.yarn_config_url + "?view=full")

    def get_impala_configs(self):
        return self.curl_get(self.impala_config_url + "?view=full")

    def enable_sentry(self):
        if self.hive_config_url is not None:
            data = {"items" : [ { "name" : "sentry_service", "value" : "sentry" } ] }
            self.curl_put(self.hive_config_url, json.dumps(data))

        if self.yarn_config_url is not None:
            data = {"items": [{"name": "min_user_id", "value": "1000"}]}
            self.curl_put(self.yarn_config_url, json.dumps(data))

        if self.impala_config_url is not None:
            data = {"items": [{"name": "sentry_service", "value": "sentry"}]}
            self.curl_put(self.impala_config_url, json.dumps(data))

        if self.hue_config_url is not None:
            data = {"items": [{"name": "sentry_service", "value": "sentry"}]}
            self.curl_put(self.hue_config_url, json.dumps(data))

        if self.solr_config_url is not None:
            data = {"items": [{"name": "sentry_service", "value": "sentry"}]}
            self.curl_put(self.solr_config_url, json.dumps(data))

