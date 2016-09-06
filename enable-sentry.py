import sys, subprocess
from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from argparse import ArgumentParser

arg_parser = ArgumentParser(description='This script enables Sentry for a given cluster in CM')
arg_parser.add_argument('cm_host', action="store",
                        help='The full CM host URL including the port number at the end')
arg_parser.add_argument('cm_user', action="store",
                        help='The username to log into CM')
arg_parser.add_argument('cm_pass', action="store",
                        help='The password to log into CM')
arg_parser.add_argument('--cluster_name', action="store", dest="cluster_name",
                        help='The name of the cluster you want to update')
args = arg_parser.parse_args()

"""
The Hive warehouse directory (/user/hive/warehouse or any path you specify as hive.metastore.warehouse.dir
in your hive-site.xml) must be owned by the Hive user and group.
"""

status = subprocess.call("kinit hdfs")

if status != 0:
    sys.exit(status=status)

subprocess.call("hdfs dfs -chmod -R 771 /user/hive/warehouse")
status = subprocess.call("hdfs dfs -chown -R hive:hive /user/hive/warehouse")

if status != 0:
    print """Unable to execute command:
hdfs dfs -chmod -R 771 /user/hive/warehouse
hdfs dfs -chown -R hive:hive /user/hive/warehouse
    """
    sys.exit(status=status)

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host+":7180", args.cm_user, args.cm_pass)

api = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=str(curl_api.version)[1:],
    cluster_name=args.cluster_name)
api.enable_sentry()
api.cluster.restart()