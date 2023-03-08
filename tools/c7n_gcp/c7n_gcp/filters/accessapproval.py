# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
"""
Access Approval Filter for GCP Project
"""
from c7n.filters.core import ValueFilter
from c7n.utils import local_session, type_schema
from c7n_gcp.resources.resourcemanager import Project
from googleapiclient.errors import HttpError


@Project.filter_registry.register('access-approval')
class AccessApprovalFilter(ValueFilter):
    """Filter Resources based on access approval configuration
    .. code-block:: yaml
      - name: project-access-approval
        resource: gcp.project
        filters:
        - type: access-approval
          key: enrolledServices.cloudProduct
          value: "all"
    """
    schema = type_schema('access-approval', rinherit=ValueFilter.schema)
    permissions = ('accessapproval.settings.get',)

    def process(self, resources, event=None):
        self.findings = self.get_findings()
        return resources if self.match(self.findings) else []

    def get_findings(self):
        session = local_session(self.manager.session_factory)
        client = session.client("accessapproval", "v1", "projects")
        project = session.get_default_project()

        try:
            findings = client.execute_query(
                'getAccessApprovalSettings',
                {'name': f"projects/{project}/accessApprovalSettings"},)
        except HttpError as ex:
            if (ex.status_code == 400 and ex.reason == "Precondition check failed.") \
                    or (ex.status_code == 404):
                # For above errors, it means either access transparency is not enabled(precondition) 
                # OR access approval is not enabled, so we want to return empty list
                findings = []
            else:
                raise ex

        return findings
