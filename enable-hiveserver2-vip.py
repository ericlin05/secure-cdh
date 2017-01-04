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

arg_parser.add_argument('--proxy-host', action="store", dest="proxy_host",
                        help='The full URL for HAProxy host')

arg_parser.add_argument('--skip-shell-command', action="store_true", dest="run_cmd",
                        help='Whether or not to skip shell commands, like "yum install" etc.')

args = arg_parser.parse_args()

if args.proxy_host is None:
    args.proxy_host = args.cm_host

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

hive_haproxy_conf = []
a = 1
for host in hs2_hosts:
    # building the load balancer hosts entries for HAProxy config file
    hive_haproxy_conf.append(
        "%s %s %s:10000" % (
            "server",
            "hive_" + str(a),
            host
        )
    )
    a = a + 1
print hive_haproxy_conf
if args.run_cmd:
    haproxy_config = open('data/haproxy-hive.cfg', 'r').read()
    print haproxy_config
    haproxy_config =  haproxy_config % ("\n    ".join(hive_haproxy_conf))

    haproxy_file_path = '/etc/haproxy/haproxy.cfg'
    print "Updating HAProxy configuration files under " + haproxy_file_path
    if os.path.exists(haproxy_file_path):
        # backup first
        shutil.copyfile(haproxy_file_path, haproxy_file_path + '.bak')
        # write to file
        f = open(haproxy_file_path, 'w')
        f.write(haproxy_config)
        f.close()


print "Updating Hive configurations"
client.enable_hive_vip(args.proxy_host)

if args.run_cmd:
    print "Restarting HAProxy services"
    status = subprocess.call("haproxy -f /etc/haproxy/haproxy.cfg", shell=True)
    if status != 0:
        sys.exit(status)



print "Restarting Hive services"
cmd = client.get_hiveserver2_service().restart()
if not cmd.wait().success:
    raise Exception("Failed to restart Impala service")


print "Done"
