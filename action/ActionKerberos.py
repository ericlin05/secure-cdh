
class ActionKerberos:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    def enable(self):
        args = self.arg_parser.parse_args()

        cm = self.api_client.api.get_cloudera_manager()
        cm.update_config({
            'SECURITY_REALM': '%s' % args.krb_realm,
            'KDC_HOST': '%s' % args.kdc_master,
            "KRB_MANAGE_KRB5_CONF": True,
            "KDC_TYPE": "MIT KDC"
        })

        # import the credentials
        print "Importing Credentials.."
        cm.import_admin_credentials(args.kdc_admin_user, args.kdc_pass).wait()

        print "Updating service configs for kerberos.."
        self.api_client.enable_kerberos()

        print "Deploying the Cluster's Kerberos client configuration.."
        cmd = self.api_client.cluster.deploy_cluster_client_config()
        if not cmd.wait().success:
            raise Exception("Failed to deploy Cluster's Kerberos client configuration")

        print "Generating Credentials"
        cmd = cm.generate_credentials()
        if not cmd.wait().success:
            raise Exception("Failed to generating credentials!")

        print "Deploying client configurations.."
        cmd = self.api_client.cluster.deploy_client_config()
        if not cmd.wait().success:
            raise Exception("Failed to deploy client configurations")

        print "Restarting Cloudera Management services.."
        cmd = cm.get_service().restart()
        if not cmd.wait().success:
            raise Exception("Failed to start Management services!")

        print "Restarting cluster"
        cmd = self.api_client.cluster.restart()

        if not cmd.wait().success:
            raise Exception("Failed to restart Cluster")
        print "Done."

