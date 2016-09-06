
class HdfsAPIClient:
    def __init__(self, service):
        self.service = service

    def enable_kerberos(self):
        self.service.update_config({
            'hadoop_security_authorization': 'true',
            'hadoop_security_authentication': 'kerberos'
        })

        # update datanode configurations
        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('DATANODE') > 0:
                role_group.update_config({
                    'dfs_datanode_port': "1004",
                    "dfs_datanode_http_port": "1006",
                    "dfs_datanode_data_dir_perm": "700"
                })
                break
