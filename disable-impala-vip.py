
from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from lib.CommonArgumentParser import CommonArgumentParser

arg_parser = CommonArgumentParser(description='This script enables Sentry for a given cluster in CM')
args = arg_parser.init().parse_args()

print "Updating Impala configurations"

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host, args.cm_user, args.cm_pass)

client = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=curl_api.get_version_number(),
    cluster_name=args.cluster_name
)

client.disable_impala_vip()

print "Restarting Impala services"
cmd = client.get_impala_service().restart()
if not cmd.wait().success:
    raise Exception("Failed to restart Impala service")

print "Done"
