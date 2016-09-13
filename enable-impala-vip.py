# https://www.cloudera.com/documentation/enterprise/latest/topics/impala_proxy.html

from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from argparse import ArgumentParser
import os, shutil, subprocess, sys

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

# Installing HAProxy server
status = subprocess.call("yum install -y haproxy", shell=True)
if status != 0:
    sys.exit(status=status)

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host+":7180", args.cm_user, args.cm_pass)

client = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=str(curl_api.version)[1:],
    cluster_name=args.cluster_name
)

impala_service = client.get_impala_service()

if impala_service is None:
    raise Exception("No Impala service available, please add Impala through Cloudera Manager")

roles = impala_service.get_all_roles()
impala_hosts = []

i = 1
for role in roles:
    if str(role.name).find('IMPALAD') >= 0:
        # building the load balancer hosts entries for HAProxy config file
        impala_hosts.append("%s %s %s" % ("server", "impala_" + str(i), client.api.get_host(role.hostRef.hostId).hostname))
        i = i + 1

haproxy_config = open('data/haproxy.cfg', 'r').read()
haproxy_config =  haproxy_config % ("\n    ".join(impala_hosts), "\n    ".join(impala_hosts))

haproxy_file_path = '/etc/haproxy/haproxy.cfg'
if os.path.exists(haproxy_file_path):
    # backup first
    shutil.copyfile(haproxy_file_path, haproxy_file_path + '.bak')
    # write to file
    f = open(haproxy_file_path, 'w')
    f.write(haproxy_config)
    f.close()

# enable load balancing in Impala
client.enable_impala_vip(args.cm_host)

# restarting HAProxy server
status = subprocess.call("haproxy -f /etc/haproxy/haproxy.cfg", shell=True)
if status != 0:
    sys.exit(status=status)

# restarting Impala services
cmd = impala_service.restart()
if not cmd.wait().success:
    raise Exception("Failed to restart Impala service")

print "Done"