from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from lib.CommonArgumentParser import CommonArgumentParser

arg_parser = CommonArgumentParser(description='This script enables Kerberos for a given cluster in CM. ' +
                                  'This assumes that KDC and Kerberos clients are installed correctly ' +
                                  'and kerberos admin principal has been created.')

arg_parser.add_argument('kdc_master', action="store",
                        help='The KDC master hostname')

arg_parser.add_argument('--kdc-admin-user', action="store", default="cloudera-scm/admin@HADOOP", dest="kdc_admin_user",
                        help='The KDC admin user pricipal, default to "cloudera-scm/admin@HADOOP"')
arg_parser.add_argument('--kdc-pass', action="store", default="cloudera", dest="kdc_pass",
                        help='The KDC admin principal password, default to "cloudera"')
arg_parser.add_argument('--krb-realm', action="store", default="HADOOP", dest="krb_realm",
                        help='The KDC REALM, default to HADOOP')

args = arg_parser.parse_args()

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host, args.cm_user, args.cm_pass)

client = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=curl_api.get_version_number(),
    cluster_name=args.cluster_name
)

cm = client.api.get_cloudera_manager()
cm.update_config({
    'SECURITY_REALM'        : '%s' % args.krb_realm,
    'KDC_HOST'              : '%s' % args.kdc_master,
    "KRB_MANAGE_KRB5_CONF"  : True,
    "KDC_TYPE"              : "MIT KDC"
})

# import the credentials
print "Importing Credentials.."
cm.import_admin_credentials(args.kdc_admin_user, args.kdc_pass).wait()

print "Updating service configs for kerberos.."
client.enable_kerberos()

print "Deploying the Cluster's Kerberos client configuration.."
cmd = client.cluster.deploy_cluster_client_config()
if not cmd.wait().success:
    raise Exception("Failed to deploy Cluster's Kerberos client configuration")

print "Generating Credentials"
cmd = cm.generate_credentials()
if not cmd.wait().success:
    raise Exception("Failed to generating credentials!")

print "Deploying client configurations.."
cmd = client.cluster.deploy_client_config()
if not cmd.wait().success:
    raise Exception("Failed to deploy client configurations")

print "Restarting Cloudera Management services.."
cmd = cm.get_service().restart()
if not cmd.wait().success:
    raise Exception("Failed to start Management services!")

print "Restarting cluster"
cmd = client.cluster.restart()

if not cmd.wait().success:
    raise Exception("Failed to restart Cluster")
print "Done."

