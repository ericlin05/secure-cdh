import os, sys
from CMAPI import CMAPI

cm_host = sys.argv[1]
cm_user = sys.argv[2]
cm_pass = sys.argv[3]
#key_tab = sys.argv[4]

# need to make /user/hive/warehouse 771 and owned by hive:hive
#sudo -u hdfs kinit -kt $KEYTAB hdfs
#sudo -u hdfs hdfs dfs -chmod -R 771 /user/hive/warehouse
#sudo -u hdfs hdfs dfs -chown -R hive:hive /user/hive/warehouse

# 1. firstly find out the CM version

cm_api = CMAPI(cm_host, cm_user, cm_pass)
print cm_api.enable_sentry()

#
# API_CMD="curl -u $CM_USER:$CM_PASS $CM_HOST/api/$VERSION"
#
# # 2. find out cluster name
# command="$API_CMD/clusters"
# echo "Running $command"
# $command

