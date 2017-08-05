import sys, subprocess
from api.APIClient import APIClient
from curl.CMAPI import CMAPI
from lib.CommonArgumentParser import CommonArgumentParser

"""
This script follows the instructions on the following page to enable HBase Authorization in CDH using CM API:
https://www.cloudera.com/documentation/enterprise/latest/topics/cdh_sg_hbase_authorization.html
"""

arg_parser = CommonArgumentParser(description='This script enables HBase Authorization for a given cluster in CM')
arg_parser.init()
args = arg_parser.parse_args()

print "Updating CM configurations.."
api = APIClient(
    args.cm_host, args.cm_user, args.cm_pass,
    cluster_name=args.cluster_name
)

if not api.has_hbase():
    raise Exception("No HBase service found, please add HBase first!!")

api.enable_hbase_authorization()
print "Finished updating CM configurations"

print "Deploying HBase client configurations.."
cmd = api.get_hbase_service().deploy_client_config()
if not cmd.wait().success:
    raise Exception("Failed to deploy HBase client configurations")


print "Restarting HBase Service.."
cmd = api.get_hbase_service().restart()
if not cmd.wait().success:
    raise Exception("Failed to restart HBase service")

print "Done."
