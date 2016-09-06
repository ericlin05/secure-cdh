
class ZookeeperAPIClient:
    def __init__(self, service):
        self.service = service

    def enable_kerberos(self):
        self.service.update_config({'enableSecurity': 'true'})