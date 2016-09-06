
class YarnAPIClient:
    def __init__(self, yarn_service):
        self.service = yarn_service

    def enable_sentry(self):
        """
        If you are using MapReduce, enable the Hive user to submit MapReduce jobs.
        1. Open the Cloudera Manager Admin Console and go to the MapReduce service.
        2. Click the Configuration tab.
        3. Select Scope > TaskTracker.
        4. Select Category > Security.
        5. Set the Minimum User ID for Job Submission property to zero (the default is 1000).
        6. Click Save Changes to commit the changes.
        7. Repeat steps 1-6 for every TaskTracker role group for the MapReduce service that is associated with Hive.
        8. Restart the MapReduce service.

        If you are using YARN, enable the Hive user to submit YARN jobs.
        1. Open the Cloudera Manager Admin Console and go to the YARN service.
        2. Click the Configuration tab.
        3. Select Scope > NodeManager.
        4. Select Category > Security.
        5. Ensure the Allowed System Users property includes the hive user. If not, add hive.
        6. Click Save Changes to commit the changes.
        7. Repeat steps 1-6 for every NodeManager role group for the YARN service that is associated with Hive.
        8. Restart the YARN service.
        """
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
