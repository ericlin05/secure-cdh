import os, shutil, subprocess, sys

class ActionImpala:
    def __init__(self, arg_parser, api_client):
        self.arg_parser = arg_parser
        self.api_client = api_client

    def disable_ha(self):
        print "Updating Impala configurations"

        self.api_client.disable_impala_vip()

        print "Restarting Impala services"
        cmd = self.api_client.get_impala_service().restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart Impala service")

        print "Done"

    def enable_ha(self):
        if self.arg_parser.run_cmd:
            # Installing HAProxy server
            print "Installing HAProxy server"
            status = subprocess.call("yum install -y haproxy", shell=True)
            if status != 0:
                sys.exit(status)

        impala_service = self.api_client.get_impala_service()

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
                        self.api_client.api.get_host(role.hostRef.hostId).hostname)
                )
                impala_shell_jdbc.append(
                    "%s %s %s:21050" % (
                        "server",
                        "impala_" + str(i),
                        self.api_client.api.get_host(role.hostRef.hostId).hostname)
                )
                i = i + 1

        if self.arg_parser.run_cmd:
            haproxy_config = open('data/haproxy.cfg', 'r').read()
            haproxy_config = haproxy_config % ("\n    ".join(impala_shell_conf), "\n    ".join(impala_shell_jdbc))

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
        self.api_client.enable_impala_vip(self.arg_parser.cm_host)

        if self.arg_parser.run_cmd:
            print "Restarting HAProxy services"
            status = subprocess.call("haproxy -f /etc/haproxy/haproxy.cfg", shell=True)
            if status != 0:
                sys.exit(status)

        print "Restarting Impala services"
        cmd = impala_service.restart()
        if not cmd.wait().success:
            raise Exception("Failed to restart Impala service")

        print "Done"
