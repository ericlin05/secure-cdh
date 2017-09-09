import os, shutil, subprocess, sys

class ActionSentry:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    """
    This script follows the instructions on the following page to enable Sentry in CDH using CM API:
    http://www.cloudera.com/documentation/enterprise/latest/topics/sg_sentry_service_config.html
    """
    def enable(self):

        args = self.arg_parser.parse_args()

        """
        The Hive warehouse directory (/user/hive/warehouse or any path you specify as hive.metastore.warehouse.dir
        in your hive-site.xml) must be owned by the Hive user and group.
        """

        if args.hdfs_update:
            print "Please enter the \"hdfs\" principal password so that we can update some HDFS directory permissions"
            status = subprocess.call("kinit hdfs", shell=True)

            if status != 0:
                sys.exit(status=status)

            print "Updating /user/hive/warehouse directory permissions 771"
            status = subprocess.call("hdfs dfs -chmod -R 771 /user/hive/warehouse", shell=True)
            if status != 0:
                message = """Unable to execute command:
            hdfs dfs -chmod -R 771 /user/hive/warehouse
                """
                raise Exception(message)

            print "Updating /user/hive/warehouse ownership to hive:hive"
            status = subprocess.call("hdfs dfs -chown -R hive:hive /user/hive/warehouse", shell=True)

            if status != 0:
                message = """Unable to execute command:
            hdfs dfs -chown -R hive:hive /user/hive/warehouse
                """
                raise Exception(message)

        print "Updating CM configurations.."

        if not self.api_client.has_sentry():
            raise Exception("No sentry service found, please add Sentry first!!")

        self.api_client.enable_sentry()
        print "Finished updating CM configurations"

        print "Deploying client configurations.."
        cmd = self.api_client.cluster.deploy_client_config()
        if not cmd.wait().success:
            raise Exception("Failed to deploy client configurations")

        print "Restarting cluster.."
        cmd = self.api_client.cluster.restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart cluster")

        print "Done."
