
class HbaseAPIClient:
    def __init__(self, service):
        self.service = service

    def enable_kerberos(self):
        self.service.update_config({
            'hbase_security_authentication': 'kerberos',
            'hbase_security_authorization': 'true',
            'hbase_superuser': 'hadoop.admin'
        })

    """
    Steps to enable HBase Authorization from below page:
    https://www.cloudera.com/documentation/enterprise/latest/topics/cdh_sg_hbase_authorization.html
    """
    def enable_authorization(self):
        # Need authentication before authorization
        self.enable_kerberos()

        safety_valve = "<property><name>hbase.security.exec.permission.checks</name><value>true</value></property>"
        self.service.update_config({
            'hbase_service_config_safety_valve': safety_valve
        })

        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('MASTER') > 0:
                role_group.update_config({
                    'hbase_coprocessor_master_classes' : 'org.apache.hadoop.hbase.security.access.AccessController',
                })

            if str(role_group.name).find('REGION') > 0:
                role_group.update_config({
                    'hbase_coprocessor_region_classes':
                        'org.apache.hadoop.hbase.security.token.TokenProvider,' +
                            'org.apache.hadoop.hbase.security.access.AccessController'
                })
