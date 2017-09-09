
from api.APIClient import APIClient
from lib.CommonArgumentParser import CommonArgumentParser
from action.ActionImpala import ActionImpala
from action.ActionSentry import ActionSentry
from action.ActionHive import ActionHive
from action.ActionHBase import ActionHBase
from action.ActionKerberos import ActionKerberos

arg_parser = CommonArgumentParser()
args = arg_parser.init().parse_args()

client = APIClient.get_api_client(args.cluster_name, args.cm_host,
                                  args.cm_user, args.cm_pass)

if args.component == 'kerberos':
    action = ActionKerberos(arg_parser, client)
    action.enable()
elif args.component == 'impala' and args.action == 'enable-ha':
    action = ActionImpala(arg_parser, client)
    action.enable_ha()
elif args.component == 'impala' and args.action == 'disable-ha':
    action = ActionImpala(arg_parser, client)
    action.disable_ha()
elif args.component == 'sentry':
    action = ActionSentry(arg_parser, client)
    action.enable()
elif args.component == 'hive' and args.action == 'enable-ha':
    action = ActionHive(arg_parser, client)
    action.enable_ha()
elif args.component == 'hbase' and args.action == 'enable-auth':
    action = ActionHBase(arg_parser, client)
    action.enable_auth()
else:
    print "Invalid component and action parameters."
