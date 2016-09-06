
class HdfsAPIClient:
    def __init__(self, service):
        self.service = service

    def enable_kerberos(self):
        self.service.update_config({
            'hadoop_security_authorization': 'true',
            'hadoop_security_authentication': 'kerberos'
        })

        # update datanode configurations
        self.service.get_role_config_group('HDFS-DATANODE-BASE').update_config({
                'dfs_datanode_port': "1004",
                "dfs_datanode_http_port": "1006",
                "dfs_datanode_data_dir_perm": "700"
            })
