import sys, subprocess
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
                        help='The name of the cluster you want to update')
arg_parser.add_argument('--skip-hdfs-cmd', action="store", dest="skip_hdfs_cmd", default=True,
                        help='The name of the cluster you want to update')
args = arg_parser.parse_args()

"""
The Hive warehouse directory (/user/hive/warehouse or any path you specify as hive.metastore.warehouse.dir
in your hive-site.xml) must be owned by the Hive user and group.
"""

if not args.skip_hdfs_cmd:
    print
    """
    Please enter the \"hdfs\" principal password so that
    we can update some HDFS directory permissions
    """
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

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host+":7180", args.cm_user, args.cm_pass)

api = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=str(curl_api.version)[1:],
    cluster_name=args.cluster_name
)

if not api.has_sentry():
    raise Exception("No sentry service found, please add Sentry first!!")

api.enable_sentry()

print "Restarting cluster.."
cmd = api.cluster.restart()
if not cmd.wait().success:
    raise Exception("Failed to restart cluster")

print "Done."