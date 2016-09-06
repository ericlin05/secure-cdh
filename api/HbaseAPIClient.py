
class HbaseAPIClient:
    def __init__(self, service):
        self.service = service

    def enable_kerberos(self):
        self.service.update_config({
            'hbase_security_authentication': 'kerberos',
            'hbase_security_authorization': 'true',
            'hbase_superuser': 'hadoop.admin'
        })
