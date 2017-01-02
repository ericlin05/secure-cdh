# https://www.cloudera.com/documentation/enterprise/latest/topics/admin_ha_hiveserver2.html

from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from lib.CommonArgumentParser import CommonArgumentParser
import os, shutil, subprocess, sys

arg_parser = CommonArgumentParser(description='This script enabled Load Balancing for ' +
                                              'HiveServer2 services for a given cluster in CM')
arg_parser.init()
arg_parser.add_argument('hs2_hosts', action="store",
                                     help='The full CM host URL including the port number at the end')

arg_parser.add_argument('--skip-shell-command', action="store_true", dest="run_cmd",
                        help='Whether or not to skip shell commands, like "yum install" etc.')

args = arg_parser.parse_args()
if args.run_cmd:
    # Installing HAProxy server
    print "Installing HAProxy server"
    status = subprocess.call("yum install -y haproxy", shell=True)
    if status != 0:
        sys.exit(status)

# use the CURL class to determine the VERSION number first
curl_api = CMAPI(args.cm_host, args.cm_user, args.cm_pass)

client = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    version=curl_api.get_version_number(),
    cluster_name=args.cluster_name
)

hiveserver2_service = client.get_hiveserver2_service()

if hiveserver2_service is None:
    raise Exception("No HiveServer2 service available, please add HiveServer2 through Cloudera Manager first")


hosts = client.api.get_all_hosts()
hs2_hosts = str(args.hs2_hosts).split(',')

existing_hs2_hosts = []
roles = hiveserver2_service.get_roles_by_type('HIVESERVER2')
for role in roles:
    host = client.api.get_host(role.hostRef.hostId)
    if host.hostname in hs2_hosts:
        existing_hs2_hosts.append(host.hostname)

if len(existing_hs2_hosts) == len(hs2_hosts):
    print "All hosts already have HS2 role installed"
else:
    i = 0
    for host in hs2_hosts:
        if host in existing_hs2_hosts:
            print "Adding HS2 to host " + host
            client.hiveserver2_create_role(host, i)
            i = i + 1
        else:
            print "Host: " + host + " already has HS2"

print "Restarting Hive services"
cmd = client.get_hiveserver2_service().restart()
if not cmd.wait().success:
    raise Exception("Failed to restart Impala service")


print "Done"
