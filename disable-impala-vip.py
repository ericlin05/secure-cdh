
from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from argparse import ArgumentParser

arg_parser = ArgumentParser(description='This script enables Sentry for a given cluster in CM')
arg_parser.add_argument('cm_host', action="store",
                        help='The full CM host URL including the port number at the end')
arg_parser.add_argument('--cm-user', action="store", dest="cm_user", default="admin",
                        help='The username to log into CM')
arg_parser.add_argument('--cm-pass', action="store", dest="cm_pass", default="admin",
                        help='The password to log into CM')

arg_parser.add_argument('--cluster-name', action="store", dest="cluster_name",
                        help='The name of the cluster you want to update, default to "None"')

args = arg_parser.parse_args()

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host+":7180", args.cm_user, args.cm_pass)

client = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=str(curl_api.version)[1:],
    cluster_name=args.cluster_name
)

client.disable_impala_vip()