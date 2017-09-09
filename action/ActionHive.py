import os, shutil, subprocess, sys

class ActionHive:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    def enable_ha(self):
        self.arg_parser.add_argument('hs2_hosts', action="store",
                                help='The full CM host URL including the port number at the end')

        self.arg_parser.add_argument('--proxy-host', action="store", dest="proxy_host",
                                help='The full URL for HAProxy host')

        self.arg_parser.add_argument('--skip-shell-command', action="store_true", dest="run_cmd",
                                help='Whether or not to skip shell commands, like "yum install" etc.')

        args = self.arg_parser.parse_args()

        if args.proxy_host is None:
            args.proxy_host = args.cm_host

        hiveserver2_service = self.api_client.get_hiveserver2_service()

        if hiveserver2_service is None:
            raise Exception("No HiveServer2 service available, please add HiveServer2 through Cloudera Manager first")

        hosts = self.api_client.api.get_all_hosts()
        hs2_hosts = str(args.hs2_hosts).split(',')

        existing_hs2_hosts = []
        roles = hiveserver2_service.get_roles_by_type('HIVESERVER2')
        for role in roles:
            host = self.api_client.api.get_host(role.hostRef.hostId)
            if host.hostname in hs2_hosts:
                existing_hs2_hosts.append(host.hostname)

        if len(existing_hs2_hosts) == len(hs2_hosts):
            print "All hosts already have HS2 role installed"
        else:
            i = 0
            for host in hs2_hosts:
                if host in existing_hs2_hosts:
                    print "Adding HS2 to host " + host
                    self.api_client.hiveserver2_create_role(host, i)
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
            haproxy_config = haproxy_config % ("\n    ".join(hive_haproxy_conf))

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
        self.api_client.enable_hive_vip(args.proxy_host)

        if args.run_cmd:
            print "Restarting HAProxy services"
            status = subprocess.call("haproxy -f /etc/haproxy/haproxy.cfg", shell=True)
            if status != 0:
                sys.exit(status)

        print "Restarting Hive services"
        cmd = self.api_client.get_hiveserver2_service().restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart Impala service")

        print "Done"
