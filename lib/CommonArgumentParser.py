
from argparse import ArgumentParser

class CommonArgumentParser(ArgumentParser):
    def init(self):
        subparsers = self.add_subparsers()

        ################################################
        # sentry related parsers
        sentry_parser = subparsers.add_parser('sentry')
        sentry_parser.add_argument('--skip-hdfs-update', action="store_false", dest="hdfs_update",
                                help='Do not trigger "hdfs" commands to update hive warehouse')
        sentry_parser.set_defaults(hdfs_update=False)
        sentry_parser.set_defaults(component='sentry')
        # currently only supports enabling sentry for a list of components, so no special actions required
        sentry_parser.set_defaults(action='')

        ################################################
        # Hive related parsers
        hive_parser = subparsers.add_parser('hive')
        hive_parser.add_argument('hs2_hosts', action="store",
                                help='The full CM host URL including the port number at the end')

        hive_parser.add_argument('--proxy-host', action="store", dest="proxy_host",
                                help='The full URL for HAProxy host')

        hive_parser.add_argument('--skip-shell-command', action="store_true", dest="run_cmd",
                                help='Whether or not to skip shell commands, like "yum install" etc.')
        hive_parser.set_defaults(component='hive')
        # currently only supports enable-ha for Hive
        hive_parser.set_defaults(action='enable-ha')

        ################################################
        # Impala related parsers
        impala_parser = subparsers.add_parser('impala')
        impala_parser.set_defaults(component='impala')
        impala_parser.add_argument('--action', action="store", dest="action", default="enable-ha",
                                   choices=['enable-ha', 'disable-ha'], help='To enable or disable Impala HA')

        ################################################
        # HBase related parsers
        hbase_parser = subparsers.add_parser('hbase')
        hbase_parser.set_defaults(component='hbase')
        # currently only supports enabling hbase authorization, so no special actions required
        hbase_parser.set_defaults(action='enable-auth')

        ################################################
        # Kerberos related parsers
        kerberos_parser = subparsers.add_parser('kerberos')
        kerberos_parser.set_defaults(component='kerberos')
        # currently only supports enabling hbase authorization, so no special actions required
        kerberos_parser.set_defaults(action='enable')

        kerberos_parser.add_argument('kdc_master', action="store",
                                help='The KDC master hostname')

        kerberos_parser.add_argument('--kdc-admin-user', action="store", default="cloudera-scm/admin@HADOOP",
                                dest="kdc_admin_user",
                                help='The KDC admin user pricipal, default to "cloudera-scm/admin@HADOOP"')
        kerberos_parser.add_argument('--kdc-pass', action="store", default="cloudera", dest="kdc_pass",
                                help='The KDC admin principal password, default to "cloudera"')
        kerberos_parser.add_argument('--krb-realm', action="store", default="HADOOP", dest="krb_realm",
                                help='The KDC REALM, default to HADOOP')

        ################################################
        # main parameters
        self.add_argument('cm_host', action="store",
                                help='The full CM host URL including the port number at the end')

        self.add_argument('--cm-user', action="store", dest="cm_user", default="admin",
                                help='The username to log into CM')
        self.add_argument('--cm-pass', action="store", dest="cm_pass", default="admin",
                                help='The password to log into CM')
    
        self.add_argument('--cluster-name', action="store", dest="cluster_name",
                                help='The name of the cluster you want to update, default to "None". ' +
                                     'If nothing is passed, it will use the first one in the cluster list.')

        return self
