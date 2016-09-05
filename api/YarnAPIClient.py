
class YarnAPIClient:
    def __init__(self, yarn_service):
        self.service = yarn_service

    def enable_sentry(self):
        role_groups = self.service.get_all_role_config_groups()
        for role_group in role_groups:
            if str(role_group.name).find('NODEMANAGE') > 0:
                role_group_config = role_group.get_config(view='full')
                system_users_list = []
                for role_group_config_name in role_group_config:
                    if role_group_config_name == 'container_executor_allowed_system_users':
                        if role_group_config[role_group_config_name].value is not None:
                            system_users_list = str(role_group_config[role_group_config_name].value).split(",")

                if 'hive' not in system_users_list:
                    system_users_list.append('hive')

                role_group.update_config({
                        'container_executor_allowed_system_users': ",".join(system_users_list),
                        'container_executor_min_user_id': '0'
                    })
