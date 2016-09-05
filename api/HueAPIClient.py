"""
Hue uses a Security app to make it easier to interact with Sentry. When you set up Hue to manage Sentry permissions,
make sure that users and groups are set up correctly. Every Hue user connecting to Sentry must have an equivalent
OS-level user account on all hosts so that Sentry can authenticate Hue users. Each OS-level user should also be
part of an OS-level group with the same name as the corresponding user's group in Hue.

For more information on using the Security app, see the related blog post.
http://gethue.com/apache-sentry-made-easy-with-the-new-hue-security-app/

Enable the Sentry service as follows:
1. Enable the Sentry service for Hive and Impala
2. Go to the Hue service.
3. Click the Configuration tab.
4. Select Scope > Hue (Service-Wide).
5. Select Category > Main.
6. Locate the Sentry Service property and select Sentry.
7. Click Save Changes to commit the changes.
8. Restart Hue.
"""
class HueAPIClient:
    def __init__(self, hue_service):
        self.service = hue_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
