
from argparse import ArgumentParser

class CommonArgumentParser(ArgumentParser):
    def init(self):
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
