import sys, subprocess
from api.APIClient import APIClient

cm_host = sys.argv[1]
cm_user = sys.argv[2]
cm_pass = sys.argv[3]

"""
The Hive warehouse directory (/user/hive/warehouse or any path you specify as hive.metastore.warehouse.dir in your hive-site.xml) must be owned by the Hive user and group.
"""

status = subprocess.call("kinit hdfs")

if status != 0:
    sys.exit(status=status)

subprocess.call("hdfs dfs -chmod -R 771 /user/hive/warehouse")
status = subprocess.call("hdfs dfs -chown -R hive:hive /user/hive/warehouse")

if status != 0:
    print """Unable to execute command:
hdfs dfs -chmod -R 771 /user/hive/warehouse
hdfs dfs -chown -R hive:hive /user/hive/warehouse
    """
    sys.exit(status=status)

api = APIClient(cm_host, cm_user, cm_pass, version=12)
api.enable_sentry()