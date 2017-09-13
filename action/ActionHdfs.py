
class ActionHdfs:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    def sentry_sync(self):
        print "Updating CM configurations.."

        if not self.api_client.has_sentry():
            raise Exception("No sentry service found, please add Sentry first!!")

        args = self.arg_parser.parse_args()
        self.api_client.enable_sentry_hdfs_sync(args.sync_prefixes)
        print "Finished updating CM configurations"

        print "Deploying client configurations.."
        cmd = self.api_client.cluster.deploy_client_config()
        if not cmd.wait().success:
            raise Exception("Failed to deploy client configurations")

        print "Restarting cluster.."
        cmd = self.api_client.cluster.restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart cluster")

        print "Done"
