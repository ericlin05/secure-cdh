# https://www.cloudera.com/documentation/enterprise/latest/topics/impala_proxy.html

from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from lib.CommonArgumentParser import CommonArgumentParser
import os, shutil, subprocess, sys

arg_parser = CommonArgumentParser(description='This script enabled Load Balancing for ' +
                                              'Impala services for a given cluster in CM')
arg_parser.init()
arg_parser.add_argument('--skip-shell-command', action="store_false", dest="run_cmd",
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

impala_service = client.get_impala_service()

if impala_service is None:
    raise Exception("No Impala service available, please add Impala through Cloudera Manager")

roles = impala_service.get_all_roles()
impala_shell_conf = []
impala_shell_jdbc = []

i = 1
for role in roles:
    if str(role.name).find('IMPALAD') >= 0:
        # building the load balancer hosts entries for HAProxy config file
        impala_shell_conf.append(
            "%s %s %s:21000" % (
                "server",
                "impala_" + str(i),
                client.api.get_host(role.hostRef.hostId).hostname)
        )
        impala_shell_jdbc.append(
            "%s %s %s:21050" % (
                "server",
                "impala_" + str(i),
                client.api.get_host(role.hostRef.hostId).hostname)
        )
        i = i + 1

if args.run_cmd:
    haproxy_config = open('data/haproxy.cfg', 'r').read()
    haproxy_config =  haproxy_config % ("\n    ".join(impala_shell_conf), "\n    ".join(impala_shell_jdbc))

    haproxy_file_path = '/etc/haproxy/haproxy.cfg'
    print "Updating HAProxy configuration files under " + haproxy_file_path
    if os.path.exists(haproxy_file_path):
        # backup first
        shutil.copyfile(haproxy_file_path, haproxy_file_path + '.bak')
        # write to file
        f = open(haproxy_file_path, 'w')
        f.write(haproxy_config)
        f.close()

# enable load balancing in Impala
print "Updating Impala configurations"
client.enable_impala_vip(args.cm_host)

if args.run_cmd:
    print "Restarting HAProxy services"
    status = subprocess.call("haproxy -f /etc/haproxy/haproxy.cfg", shell=True)
    if status != 0:
        sys.exit(status)

print "Restarting Impala services"
cmd = impala_service.restart()
if not cmd.wait().success:
    raise Exception("Failed to restart Impala service")

print "Done"
