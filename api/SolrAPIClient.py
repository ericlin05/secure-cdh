"""
Enabling the Sentry Service for Solr
1. Go to the Solr service.
2. Click the Configuration tab.
3. Select Scope > Solr (Service-Wide).
4.Select Category > Main.
5. Locate the Sentry Service property and select Sentry.
6. Click Save Changes to commit the changes.
7. Restart Solr.
"""
class SolrAPIClient:
    def __init__(self, solr_service):
        self.service = solr_service

    def enable_sentry(self):
        self.service.update_config({'sentry_service': 'sentry'})
