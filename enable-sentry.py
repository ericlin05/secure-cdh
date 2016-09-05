import sys
from api.APIClient import APIClient

cm_host = sys.argv[1]
cm_user = sys.argv[2]
cm_pass = sys.argv[3]

api = APIClient(cm_host, cm_user, cm_pass, version=12)
api.enable_sentry()