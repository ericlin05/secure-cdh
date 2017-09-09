
class ActionHBase:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    """
    This script follows the instructions on the following page to enable HBase Authorization in CDH using CM API:
    https://www.cloudera.com/documentation/enterprise/latest/topics/cdh_sg_hbase_authorization.html
    """
    def enable_auth(self):
        print "Updating CM configurations.."

        if not self.api_client.has_hbase():
            raise Exception("No HBase service found, please add HBase first!!")

        self.api_client.enable_hbase_authorization()
        print "Finished updating CM configurations"

        print "Deploying HBase client configurations.."
        cmd = self.api_client.get_hbase_service().deploy_client_config()
        if not cmd.wait().success:
            raise Exception("Failed to deploy HBase client configurations")

        print "Restarting HBase Service.."
        cmd = self.api_client.get_hbase_service().restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart HBase service")

        print "Done."
