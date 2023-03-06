# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
from c7n_gcp.query import QueryResourceManager, TypeInfo
from c7n_gcp.provider import resources


@resources.register('access-approval')
class AccessApproval(QueryResourceManager):
    """GCP Access Approval Settings
    https://cloud.google.com/cloud-provider-access-management/access-approval/docs/reference/rest/v1/projects/getAccessApprovalSettings
    """
    class resource_type(TypeInfo):
        service = 'accessapproval'
        version = 'v1'
        component = 'projects'
        enum_spec = ('getAccessApprovalSettings', '[@]', None)
        scope = 'project'
        scope_key = 'name'
        scope_template = 'projects/{}/accessApprovalSettings'
        name = id = "name"
        default_report_fields = ["name", "notificationEmails", "enrolledServices"]
        permissions = ('accessapproval.settings.get',)
        asset_type = "accessapproval.googleapis.com/projects"
