# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

from c7n_azure.provider import resources
from c7n_azure.resources.arm import ArmResourceManager


@resources.register('spring-service-instance')
class SpringServiceInstance(ArmResourceManager):
    """Azure Spring Service Instance Resource

    :example:

    Returns Spring Service Instance resources

    .. code-block:: yaml

         policies:
          - name: basic-spring-service-instance
            resource: azure.spring-service-instance

    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Compute']

        service = 'azure.mgmt.appplatform'
        client = 'AppPlatformManagementClient'
        enum_spec = ('services', 'list_by_subscription', None)
        default_report_fields = (
            'name',
            'location',
            'resourceGroup'
        )
        resource_type = 'Microsoft.AppPlatform/Spring'
